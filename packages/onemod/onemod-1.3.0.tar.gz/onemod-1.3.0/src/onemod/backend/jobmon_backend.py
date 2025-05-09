"""Functions to run pipelines and stages with Jobmon.

Examples
--------
Compute resources can be passed as a dictionary or a path to a resources
file (e.g., json, toml, yaml).

Required tool resources:

.. code-block:: yaml

    tool_resources:
      {cluster_name}:
        project: {proj_name}
        queue: {queue_name}

To test workflow on a dummy cluster (i.e., run workflow without running
tasks), use:

.. code-block:: yaml

    tool_resources:
      dummy:
        queue: null.q

Optional stage resources can be specified at the stage or stage + method
level:

    task_template_resources:
      {stage_name}:
        {cluster_name}:
            ...
      {stage_name}_{collect}:
        {cluster_name}:
            ...

See Jobmon documentation for additional resources and default values.

"""
# TODO: Optional stage-specific Python environments
# TODO: User-defined max_attempts
# TODO: Could dependencies be method specific?
# TODO: should we check resources format, minimum resources, cluster?

import itertools
import sys
from pathlib import Path
from typing import Any, Literal

from jobmon.client.api import Tool
from jobmon.client.task import Task
from jobmon.client.task_template import TaskTemplate
from jobmon.client.workflow import Workflow
from pydantic import ConfigDict, validate_call

from onemod.backend.utils import (
    check_input_exists,
    check_method,
    collect_results,
)
from onemod.fsutils.config_loader import ConfigLoader
from onemod.pipeline import Pipeline
from onemod.stage import Stage


@validate_call
def evaluate_with_jobmon(
    model: Pipeline | Stage,
    method: Literal["run", "fit", "predict", "collect"],
    cluster: str,
    resources: Path | str | dict[str, Any],
    python: Path | str | None = None,
    stages: list[str] | None = None,
    subsets: dict[str, Any | list[Any]] | None = None,
    paramsets: dict[str, Any | list[Any]] | None = None,
    collect: bool | None = None,
    task_prefix: str | None = None,
    task_attributes: dict[str, Any] = dict(),
    template_prefix: str | None = None,
    max_attempts: int = 1,
    **kwargs,
) -> None:
    """Evaluate pipeline or stage method with Jobmon.

    Parameters
    ----------
    model : Pipeline or Stage
        Pipeline or stage instance.
    method : {'run', 'fit', 'predict', 'collect'}
        Name of method to evalaute.
    cluster : str
        Cluster name.
    resources : dict, Path, or str
        Path to resources file or dictionary of compute resources.
    python : Path or str, optional
        Path to Python environment. If None, use sys.executable.
        Default is None.
    **kwargs
        Additional keyword arguments passed to stage methods. If `model`
        is a `Pipeline` instance, use format`stage={arg_name: arg_value}`.

    Pipeline Parameters
    -------------------
    stages : list of str, optional
        Names of stages to evaluate if `model` is a `Pipeline` instance.
        If None, evaluate pipeline stages. Default is None.

    Stage Parameters
    ----------------
    subsets : dict, optional
        Submodel data subsets to evaluate if `model` is a `Stage`
        instance. If None, evaluate all data subsets. Default is None.
    paramsets : dict, optional
        Submodel parameter sets to evaluate if `model` is a `Stage`
        instance. If None, evaluate all parameter sets. Default is None.
    collect : bool, optional
        Whether to collect submodel results if `model` is a `Stage`
        instance. If `subsets` and `paramsets` are both None, default is
        True, otherwise default is False.

    Jobmon Parameters
    -----------------
    task_prefix : str, optional
        Optional prefix to append to task names. Default is None, no
        prefix.
    task_attributes : dict
        Dictionary containing task attribute names and values. Note that
        the task attributes will be shared across all tasks in any given
        Workflow. Default is an empty dict, no task attributes.
    template_prefix : str, optional
        Optional prefix to append to task template name. Default is None,
        no prefix.
    max_attempts : int
        Maximum number of attempts for a task. Default is 1.

    """
    check_method(model, method)
    check_input_exists(model, stages)
    if python is None:
        python = str(sys.executable)

    resources_dict = get_resources(resources)
    workflow = create_workflow(model.name, method, cluster, resources_dict)
    add_tasks_to_workflow(
        model=model,
        workflow=workflow,
        method=method,
        resources=resources_dict,
        python=python,
        stages=stages,
        subsets=subsets,
        paramsets=paramsets,
        collect=collect,
        task_prefix=task_prefix,
        task_attributes=task_attributes,
        template_prefix=template_prefix,
        max_attempts=max_attempts,
        **kwargs,
    )
    run_workflow(workflow)


@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
def add_tasks_to_workflow(
    model: Pipeline | Stage,
    workflow: Workflow,
    method: Literal["run", "fit", "predict", "collect"],
    resources: Path | str | dict[str, Any],
    python: Path | str | None = None,
    stages: list[str] | None = None,
    subsets: dict[str, Any | list[Any]] | None = None,
    paramsets: dict[str, Any | list[Any]] | None = None,
    collect: bool | None = None,
    task_prefix: str | None = None,
    task_attributes: dict[str, Any] = dict(),
    template_prefix: str | None = None,
    max_attempts: int = 1,
    external_upstream_tasks: list[Task] | None = None,
    **kwargs,
) -> None:
    """Add Pipeline tasks to an existing Jobmon Workflow.

    Note that this is a publically available function, be careful of
    breaking changes to the API or functionality.

    Parameters
    ----------
    workflow : Workflow
        Instantiated Jobmon workflow. Add new tasks to an existing Jobmon
        workflow rather than creating a new workflow. Does not run the
        workflow, only adds the tasks.
    model : Pipeline or Stage
        Pipeline or stage instance.
    method : {'run', 'fit', 'predict', 'collect'}
        Name of method to evalaute.
    resources : dict, Path, or str
        Path to resources file or dictionary of compute resources.
    python : Path or str, optional
        Path to Python environment. If None, use sys.executable.
        Default is None.
    **kwargs
        Additional keyword arguments passed to stage methods. If `model`
        is a `Pipeline` instance, use format`stage={arg_name: arg_value}`.

    Pipeline Parameters
    -------------------
    stages : list of str, optional
        Names of stages to evaluate if `model` is a `Pipeline` instance.
        If None, evaluate pipeline stages. Default is None.

    Stage Parameters
    ----------------
    subsets : dict, optional
        Submodel data subsets to evaluate if `model` is a `Stage`
        instance. If None, evaluate all data subsets. Default is None.
    paramsets : dict, optional
        Submodel parameter sets to evaluate if `model` is a `Stage`
        instance. If None, evaluate all parameter sets. Default is None.
    collect : bool, optional
        Whether to collect submodel results if `model` is a `Stage`
        instance. If `subsets` and `paramsets` are both None, default is
        True, otherwise default is False.

    Jobmon Parameters
    -----------------
    task_prefix : str, optional
        Optional prefix to append to task names. Default is None, no
        prefix.
    task_attributes : dict
        Dictionary containing task attribute names and values. Note that
        the task attributes will be shared across all tasks in any given
        Workflow. Default is an empty dict, no task attributes.
    template_prefix : str, optional
        Optional prefix to append to task template name. Default is None,
        no prefix.
    max_attempts : int
        Maximum number of attempts for a task. Default is 1.
    external_upstream_tasks : list, optional
        List of Jobmon tasks external to the OneMod Stages or Pipeline that
        should be treated as upstream dependencies of the new tasks. Default
        is no external upstream tasks.

    """
    check_method(model, method)
    check_input_exists(model, stages)
    if python is None:
        python = str(sys.executable)

    resources_dict = get_resources(resources)
    tasks = get_tasks(
        model=model,
        method=method,
        tool=workflow.tool,
        resources=resources_dict,
        python=python,
        stages=stages,
        subsets=subsets,
        paramsets=paramsets,
        collect=collect,
        task_prefix=task_prefix,
        task_attributes=task_attributes,
        template_prefix=template_prefix,
        max_attempts=max_attempts,
        external_upstream_tasks=external_upstream_tasks,
        **kwargs,
    )
    workflow.add_tasks(tasks)


def get_resources(resources: Path | str | dict[str, Any]) -> dict[str, Any]:
    """Get dictionary of compute resources.

    Parameters
    ----------
    resources : Path, str, or dict
        Path to resources file or dictionary of compute resources.

    Returns
    -------
    dict
        Dictionary of compute resources.

    """
    if isinstance(resources, (Path, str)):
        config_loader = ConfigLoader()
        return config_loader.load(Path(resources))
    return resources


def create_workflow(
    name: str,
    method: Literal["run", "fit", "predict", "collect"],
    cluster: str,
    resources: dict[str, Any],
) -> Workflow:
    """Create and return workflow.

    Parameters
    ----------
    name : str
        Pipeline or stage name.
    method : str
        Name of method being evaluated.
    cluster : str
        Cluster name.
    resources : dict
        Dictionary of compute resources.

    Returns
    -------
    Workflow
        Jobmon workflow.

    """
    tool = get_tool(name, method, cluster, resources)
    workflow = tool.create_workflow(name=f"{name}_{method}")
    return workflow


def get_tool(
    name: str, method: str, cluster: str, resources: dict[str, Any]
) -> Tool:
    """Get Jobmon tool.

    Parameters
    ----------
    name : str
        Pipeline or stage name.
    method : str
        Name of method to evaluate.
    cluster : str
        Cluster name.
    resources : dict
        Dictionary of compute resources.

    Returns
    -------
    Tool
        Jobmon tool.

    """
    tool = Tool(name=f"{name}_{method}")
    tool.set_default_cluster_name(cluster)
    tool.set_default_compute_resources_from_dict(
        cluster, resources["tool_resources"][cluster]
    )
    return tool


def get_tasks(
    model: Pipeline | Stage,
    method: str,
    tool: Tool,
    resources: dict[str, Any],
    python: Path | str,
    stages: list[str] | None,
    subsets: dict[str, Any | list[Any]] | None,
    paramsets: dict[str, Any | list[Any]] | None,
    collect: bool | None,
    task_prefix: str | None,
    task_attributes: dict[str, Any],
    template_prefix: str | None,
    max_attempts: int,
    external_upstream_tasks: list[Task] | None = None,
    **kwargs,
) -> list[Task]:
    """Get Jobmon tasks.

    Parameters
    ----------
    model : Pipeline or Stage
        Pipeline or stage instance.
    method : str
        Name of method to evaluate.
    tool : Tool
        Jobmon tool.
    resources : dict
        Dictionary of compute resources.
    python : Path or str
        Path to Python environment.
    **kwargs
        Additional keyword arguments passed to stage methods.

    Pipeline Parameters
    -------------------
    stages : list of str or None
        Name of stages to evaluate if `model` is a pipeline instance. If
        None, evaluate all pipeline stages.

    Stage Parameters
    ----------------
    subsets : dict or None
        Submodel data subsets to evaluate if `model` is a `Stage`
        instance. If None, evaluate all data subsets.
    paramsets : dict or None
        Submodel parameter sets to evaluate if `model` is a `Stage`
        instance. If None, evaluate all parameter sets.
    collect : bool or None
        Whether to collect submodel results if `model` is a `Stage`
        instance.

    Jobmon Parameters
    -----------------
    task_prefix : str, optional
        Optional prefix to append to task names.
    task_attributes : dict, optional
        Optional dictionary containing task attribute names and values.
    template_prefix : str, optional
        Optional prefix to append to task template name.
    max_attempts : int
        Maximum number of attempts for a task.
    external_upstream_tasks : list, optional
        List of Jobmon tasks external to the OneMod Stages or Pipeline that
        should be treated as upstream dependencies of the new tasks. Default
        None, no external upstreams.

    Returns
    -------
    list of Task
        List of Jobmon tasks.

    """
    if isinstance(model, Pipeline):
        return get_pipeline_tasks(
            pipeline=model,
            method=method,
            tool=tool,
            resources=resources,
            python=python,
            stages=stages,
            external_upstream_tasks=external_upstream_tasks,
            task_prefix=task_prefix,
            task_attributes=task_attributes,
            template_prefix=template_prefix,
            max_attempts=max_attempts,
            **kwargs,
        )
    return get_stage_tasks(
        stage=model,
        method=method,
        tool=tool,
        resources=resources,
        python=python,
        task_prefix=task_prefix,
        task_attributes=task_attributes,
        template_prefix=template_prefix,
        max_attempts=max_attempts,
        subsets=subsets,
        paramsets=paramsets,
        collect=collect,
        upstream_tasks=external_upstream_tasks,
        **kwargs,
    )


def get_pipeline_tasks(
    pipeline: Pipeline,
    method: str,
    tool: Tool,
    resources: dict[str, Any],
    python: Path | str,
    stages: list[str] | None,
    external_upstream_tasks: list[Task] | None,
    task_prefix: str | None,
    task_attributes: dict[str, Any],
    template_prefix: str | None,
    max_attempts: int,
    **kwargs,
) -> list[Task]:
    """Get pipeline stage tasks.

    Parameters
    ----------
    pipeline : Pipeline
        Pipeline instance.
    method : str
        Name of method to evaluate.
    tool : Tool
        Jobmon tool.
    resources : dict
        Dictionary of compute resources.
    python : Path or str
        Path to Python environment.
    stages : list of str or None
        Name of stages to evaluate. If None, evaluate all pipeline
        stages.
    external_upstream_tasks : list, optional
        List of Jobmon tasks external to the OneMod Stages or Pipeline that
        should be treated as upstream dependencies of the new tasks.
    task_prefix : str, optional
        Optional prefix to append to task names.
    task_attributes : dict, optional
        Optional dictionary containing task attribute names and values.
    template_prefix : str, optional
        Optional prefix to append to task template name.
    max_attempts : int
        Maximum number of attempts for a task.
    **kwargs
        Additional keyword arguments passed to stage methods.

    Returns
    -------
    list of Task
        List of pipeline stage tasks.

    """
    tasks = []
    task_dict: dict[str, list[Task]] = {}
    task_dict["external"] = external_upstream_tasks or []

    for stage_name in pipeline.get_execution_order(stages):
        stage = pipeline.stages[stage_name]
        if method not in stage.skip:
            upstream_tasks = get_upstream_tasks(
                stage=stage,
                method=method,
                stage_dict=pipeline.stages,
                task_dict=task_dict,
                stages=stages,
                task_prefix=task_prefix,
                template_prefix=template_prefix,
            )
            task_dict[stage_name] = get_stage_tasks(
                stage=stage,
                method=method,
                tool=tool,
                resources=resources,
                python=python,
                task_prefix=task_prefix,
                task_attributes=task_attributes,
                template_prefix=template_prefix,
                max_attempts=max_attempts,
                upstream_tasks=upstream_tasks,
                **kwargs,
            )
            tasks.extend(task_dict[stage_name])

    return tasks


def get_upstream_tasks(
    stage: Stage,
    method: str,
    stage_dict: dict[str, Stage],
    task_dict: dict[str, list[Task]],
    stages: list[str] | None,
    task_prefix: str | None,
    template_prefix: str | None,
) -> list[Task]:
    """Get upstream tasks for current stage.

    Parameters
    ----------
    stage : Stage
        Current stage instance.
    method : str
        Name of method to evaluate.
    stage_dict : dict
        Dictionary of all pipeline stages.
    task_dict : dict
        Dictionary of all upstream stage tasks.
    stages : list of str or None
        Names of all pipeline stages being evaluated. If None, assume
        all stages are being evaluated.
    task_prefix : str, optional
        Optional prefix to filter upstream tasks with.
    template_prefix : str, optional
        Optional prefix to filter task templates with.

    Returns
    -------
    list of Task
        Upstream stage tasks for current stage.

    Notes
    -----
    * Only include tasks corresponding to the current stage's
      dependencies that are included in `stages`.
    * If an upstream stage has submodels and `method` is in the
      upstream's `collect_after`, only include the task corresponding to
      the upstream's `collect` method.
    * If there are no upstream tasks, add any external tasks as upstream.

    """
    upstream_tasks = []

    for upstream_name in stage.dependencies:
        if stages is not None and upstream_name not in stages:
            # upstream stage is not being evaluated
            continue

        upstream_stage = stage_dict[upstream_name]

        # Filter possible upstreams using task and template prefixes
        possible_upstream_tasks = task_dict[upstream_name]
        if task_prefix:
            possible_upstream_tasks = [
                possible_upstream_task
                for possible_upstream_task in possible_upstream_tasks
                if possible_upstream_task.name.startswith(task_prefix)
            ]
        if template_prefix:
            possible_upstream_tasks = [
                possible_upstream_task
                for possible_upstream_task in possible_upstream_tasks
                if possible_upstream_task.node.task_template_version.task_template.template_name.startswith(
                    template_prefix
                )
            ]
        if method not in upstream_stage.skip:
            if (
                upstream_stage.has_submodels
                and method in upstream_stage.collect_after
            ):
                # only include task corresponding to 'collect' method
                upstream_tasks.append(possible_upstream_tasks[-1])
            else:
                upstream_tasks.extend(possible_upstream_tasks)

    # if there are no upstream tasks, add external upstream tasks
    if not upstream_tasks:
        upstream_tasks = task_dict.get("external", [])

    return upstream_tasks


def get_stage_tasks(
    stage: Stage,
    method: str,
    tool: Tool,
    resources: dict[str, Any],
    python: Path | str,
    task_prefix: str | None,
    task_attributes: dict[str, Any],
    template_prefix: str | None,
    max_attempts: int,
    subsets: dict[str, Any | list[Any]] | None = None,
    paramsets: dict[str, Any | list[Any]] | None = None,
    collect: bool | None = None,
    upstream_tasks: list[Task] | None = None,
    **kwargs,
) -> list[Task]:
    """Get stage tasks.

    Parameters
    ----------
    stage : Stage
        Stage instance.
    method : str
        Name of method to evaluate.
    tool : Tool
        Jobmon tool.
    resources : dict
        Dictionary of compute resources.
    python : Path or str
        Path to Python environment.
    subsets : dict, optional
        Submodel data subsets to evaluate. If None, evaluate all data
        subsets. Default is None.
    paramsets : dict, optional
        Submodel parameter sets to evaluate. If None, evaluate all
        parameter sets. Default is None.
    collect : bool, optional
        Whether to collect submodel results if `model` is a `Stage`
        instance. If `subsets` and `paramsets` are both None, default is
        True, otherwise default is False.
    upstream_tasks : list of Task or None, optional
        List of upstream stage tasks. Default is None.
    task_prefix : str, optional
        Optional prefix to append to task names.
    task_attributes : dict, optional
        Optional dictionary containing task attribute names and values.
    template_prefix : str, optional
        Optional prefix to append to task template name.
    max_attempts : int
        Maximum number of attempts for a task.
    **kwargs
        Additional keyword arguments passed to stage method.

    Returns
    -------
    list of Task
        List of stage tasks.

    """
    if upstream_tasks is None:
        upstream_tasks = []

    entrypoint = str(Path(python).parent / "onemod")
    config_path = str(stage.dataif.get_path("config"))
    submodel_args = get_submodel_args(stage, method, subsets, paramsets)

    task_template = get_task_template(
        stage.name,
        method,
        tool,
        resources,
        list(submodel_args.keys()),
        template_prefix=template_prefix,
        **kwargs,
    )

    task_name = (
        f"{task_prefix}_{stage.name}_{method}"
        if task_prefix
        else f"{stage.name}_{method}"
    )
    if submodel_args:
        # NOTE: TaskTemplate.create_tasks can only be called once per
        # instantiated TaskTemplate, but workflows that contain multiple
        # OneMod Pipelines with overlapping TaskTemplates will need to
        # add tasks to the same template multiple times. To get around
        # this, we need to use TaskTemplate.create_task (not tasks)
        # instead. This means we need to generate all combinations of
        # submodel args and loop over them in task creation.
        submodel_keys, submodel_values = zip(*submodel_args.items())
        submodel_arg_combinations = [
            dict(zip(submodel_keys, submodel_valueset))
            for submodel_valueset in itertools.product(*submodel_values)
        ]
        tasks = [
            task_template.create_task(
                name=task_name,
                upstream_tasks=upstream_tasks,
                task_attributes=task_attributes,
                max_attempts=max_attempts,
                entrypoint=entrypoint,
                config=config_path,
                method=method,
                stages=stage.name,
                **{**submodel_arg_combination, **kwargs},
            )
            for submodel_arg_combination in submodel_arg_combinations
        ]
    else:
        tasks = [
            task_template.create_task(
                name=task_name,
                upstream_tasks=upstream_tasks,
                task_attributes=task_attributes,
                max_attempts=max_attempts,
                entrypoint=entrypoint,
                config=config_path,
                method=method,
                stages=stage.name,
                **kwargs,
            )
        ]

    if collect_results(stage, method, subsets, paramsets, collect):
        tasks.extend(
            get_stage_tasks(
                stage=stage,
                method="collect",
                tool=tool,
                resources=resources,
                python=python,
                task_prefix=task_prefix,
                task_attributes=task_attributes,
                template_prefix=template_prefix,
                max_attempts=max_attempts,
                upstream_tasks=tasks,
            )
        )

    return tasks


def get_submodel_args(
    stage: Stage,
    method: str,
    subsets: dict[str, Any | list[Any]] | None,
    paramsets: dict[str, Any | list[Any]] | None,
) -> dict[str, list[str]]:
    """Get dictionary of subset and/or paramset values.

    If stage has submodels and `method` is not 'collect', additional
    args for 'subsets' and/or 'paramsets' are included in the command
    template.

    Parameters
    ----------
    stage : Stage
        Stage instance.
    method : str
        Method being evaluated.
    subsets : dict or None.
        Submodel data subsets to evaluate. If None, evaluate all data
        subsets.
    paramsets : dict or None
        Submodel parameter sets to evaluate. If None, evaluate all
        parameter sets.

    Returns
    -------
    dict
        Dictionary of subset and/or paramset values as strings.

    """
    submodel_args = {}
    if stage.has_submodels and method != "collect":
        # Get data subsets
        if (filtered_subsets := stage.subsets) is not None:
            if subsets is not None:
                filtered_subsets = stage.get_subset(filtered_subsets, subsets)
            submodel_args["subsets"] = [
                str(subset)
                for subset in filtered_subsets.to_dict(orient="records")
            ]

        # Get parameter sets
        if (filtered_paramsets := stage.paramsets) is not None:
            if paramsets is not None:
                filtered_paramsets = stage.get_subset(
                    filtered_paramsets, paramsets
                )
            submodel_args["paramsets"] = [
                str(paramset)
                for paramset in filtered_paramsets.to_dict(orient="records")
            ]

    return submodel_args


def get_task_template(
    stage_name: str,
    method: str,
    tool: Tool,
    resources: dict[str, Any],
    submodel_args: list[str],
    template_prefix: str | None,
    **kwargs,
) -> TaskTemplate:
    """Get stage task template.

    If the Jobmon Tool already has an active task template with the same
    name, use that task template.

    Parameters
    ----------
    stage_name : str
        Stage name.
    method : str
        Name of method being evaluated.
    tool : Tool
        Jobmon tool.
    resources : dict
        Dictionary of compute resources.
    submodel_args : list of str
        List including 'subsets' and/or 'paramsets'.
    template_prefix : str, optional
        Optional prefix to append to task template name.
    **kwargs
        Additional keyword arguments passed to stage method.

    Returns
    -------
    TaskTemplate
        Stage task template.

    """
    template_name = (
        f"{template_prefix}_{stage_name}_{method}"
        if template_prefix
        else f"{stage_name}_{method}"
    )

    command_template = get_command_template(method, submodel_args, **kwargs)
    task_args = ["method", "stages"] + list(kwargs.keys())
    # NOTE: Config is a node arg for the purposes of running multiple
    # OneMod models in a single workflow; since each model will have
    # a separate config, this allows a user to keep the same task
    # template name across all models in a given workflow.
    node_args = ["config"] + submodel_args

    task_template = tool.get_task_template(
        template_name=template_name,
        command_template=command_template,
        op_args=["entrypoint"],
        task_args=task_args,
        node_args=node_args,
    )

    task_resources = get_task_resources(
        resources, tool.default_cluster_name, stage_name, method
    )
    if task_resources:
        task_template.set_default_compute_resources_from_dict(
            tool.default_cluster_name, task_resources
        )

    return task_template


def get_command_template(
    method: str, submodel_args: list[str], **kwargs
) -> str:
    """Get stage command template.

    All stages methods are called via `onemod.main.evaluate()`. If stage
    has submodels and `method` is not 'collect', additional args for
    'subsets' and/or 'paramsets' are included in the command template.

    Parameters
    ----------
    method : str
        Name of method being evaluated.
    submodel_args : list of str
        List including 'subsets' and/or 'paramsets'.
    **kwargs
        Additional keyword arguments passed to stage method.

    Returns
    -------
    str
        Stage command template.

    # TODO: collapse into one list

    """
    command_template = (
        "{entrypoint} --config {config} --method {method} --stages {stages}"
    )

    if method != "collect":
        for key, value in kwargs.items():
            if isinstance(value, (dict, list, set, tuple)):
                command_template += f" --{key} '{{{key}}}'"
            else:
                command_template += f" --{key} {{{key}}}"

        for arg in submodel_args:
            command_template += f" --{arg} '{{{arg}}}'"

    return command_template


def get_task_resources(
    resources: dict[str, Any], cluster: str, stage_name: str, method: str
) -> dict[str, Any]:
    """Get task-specific resources.

    Parameters
    ----------
    resources : dict
        Dictionary of compute resources.
    cluster : str
        Cluster name.
    stage_name : str
        Stage name.
    method : str
        Name of method being evaluated.

    Returns
    -------
    dict
        Task-specific resources.

    """
    task_resources = resources.get("task_template_resources", {})
    stage_resources = task_resources.get(stage_name, {})
    method_resources = task_resources.get(f"{stage_name}_{method}", {})
    return {
        **stage_resources.get(cluster, {}),
        **method_resources.get(cluster, {}),
    }


def run_workflow(workflow: Workflow) -> None:
    """Run workflow.

    Parameters
    ----------
    workflow : Workflow
        Jobmon workflow to run.

    """
    workflow.bind()
    print(f"Starting workflow {workflow.workflow_id}")
    status = workflow.run()
    if status != "D":
        raise ValueError(f"Workflow {workflow.workflow_id} failed")
    else:
        print(f"Workflow {workflow.workflow_id} finished")
