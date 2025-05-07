# This file creates scaffolds for agents and functions
# agentmap/scaffold.py

"""
Agent scaffolding utility for AgentMap.
Creates Python class files for custom agents and function stubs based on CSV input.
"""

import csv
from logging import getLogger

logger = getLogger(__name__)

from pathlib import Path
from typing import Dict, List, Optional, Union

from agentmap.agents import get_agent_class
from agentmap.config import (get_csv_path, get_custom_agents_path,
                             get_functions_path)
from agentmap.utils.common import extract_func_ref


def load_template(template_name: str) -> str:
    """Load a template file from the templates directory."""
    templates_dir = Path(__file__).parent.parent / "templates"
    template_path = templates_dir / f"{template_name}.py.txt"
    if not template_path.exists():
        raise FileNotFoundError(f"Template {template_name} not found at {template_path}")
    return template_path.read_text()


def collect_agent_info(
    csv_path: Path, 
    graph_name: Optional[str] = None
) -> Dict[str, Dict]:
    """
    Collect information about agents from the CSV file.
    
    Args:
        csv_path: Path to the CSV file
        graph_name: Optional graph name to filter by
        
    Returns:
        Dictionary mapping agent types to their information
    """
    agent_info: Dict[str, Dict] = {}
    
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip rows that don't match our graph filter
            if graph_name and row.get("GraphName", "").strip() != graph_name:
                continue
                
            # Collect agent information
            agent_type = row.get("AgentType", "").strip()
            if agent_type and not get_agent_class(agent_type):
                node_name = row.get("Node", "").strip()
                context = row.get("Context", "").strip()
                prompt = row.get("Prompt", "").strip()
                input_fields = [x.strip() for x in row.get("Input_Fields", "").split("|") if x.strip()]
                output_field = row.get("Output_Field", "").strip()
                
                if agent_type not in agent_info:
                    agent_info[agent_type] = {
                        "node_name": node_name,
                        "context": context,
                        "prompt": prompt,
                        "input_fields": input_fields,
                        "output_field": output_field
                    }
    
    return agent_info


def collect_function_info(
    csv_path: Path, 
    graph_name: Optional[str] = None
) -> Dict[str, Dict]:
    """
    Collect information about functions from the CSV file.
    
    Args:
        csv_path: Path to the CSV file
        graph_name: Optional graph name to filter by
        
    Returns:
        Dictionary mapping function names to their information
    """
    func_info: Dict[str, Dict] = {}
    
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip rows that don't match our graph filter
            if graph_name and row.get("GraphName", "").strip() != graph_name:
                continue
                
            # Collect function information
            for col in ["Edge", "Success_Next", "Failure_Next"]:
                func = extract_func_ref(row.get(col, ""))
                if func:
                    node_name = row.get("Node", "").strip()
                    context = row.get("Context", "").strip()
                    input_fields = [x.strip() for x in row.get("Input_Fields", "").split("|") if x.strip()]
                    output_field = row.get("Output_Field", "").strip()
                    success_next = row.get("Success_Next", "").strip()
                    failure_next = row.get("Failure_Next", "").strip()
                    
                    if func not in func_info:
                        func_info[func] = {
                            "node_name": node_name,
                            "context": context,
                            "input_fields": input_fields,
                            "output_field": output_field,
                            "success_next": success_next,
                            "failure_next": failure_next
                        }
    
    return func_info


def generate_field_access(input_fields: List[str]) -> str:
    """
    Generate code to access fields from the inputs dictionary.
    
    Args:
        input_fields: List of input field names
        
    Returns:
        String containing lines of Python code to access fields
    """
    access_lines = []
    for field in input_fields:
        access_lines.append(f"        {field} = inputs.get(\"{field}\")")
    
    if not access_lines:
        access_lines = ["        # No specific input fields defined in the CSV"]
    
    return "\n".join(access_lines)


def generate_context_fields(input_fields: List[str], output_field: str) -> str:
    """
    Generate documentation about available fields in the state.
    
    Args:
        input_fields: List of input field names
        output_field: Output field name
        
    Returns:
        String containing documentation lines
    """
    context_fields = []
    
    for field in input_fields:
        context_fields.append(f"    - {field}: Input from previous node")
    
    if output_field:
        context_fields.append(f"    - {output_field}: Expected output to generate")
    
    if not context_fields:
        context_fields = ["    No specific fields defined in the CSV"]
    
    return "\n".join(context_fields)


def scaffold_agent(
    agent_type: str, 
    info: Dict, 
    output_path: Path
) -> bool:
    """
    Create a scaffold file for an agent.
    
    Args:
        agent_type: Type of agent to scaffold
        info: Information about the agent
        output_path: Directory to create agent class in
        
    Returns:
        True if agent was scaffolded, False if it already existed
    """
    class_name = agent_type + "Agent"
    file_name = f"{agent_type.lower()}_agent.py"
    path = output_path / file_name
    
    if path.exists():
        return False
    
    # Generate input field access code
    input_field_access = generate_field_access(info["input_fields"])
    
    # Load template
    template = load_template("agent_template")
    
    # Create agent file
    with path.open("w") as out:
        out.write(template.format(
            class_name=class_name,
            context_description=info["context"] or "No context description provided",
            input_fields=", ".join(info["input_fields"]) or "None specified",
            output_field=info["output_field"] or "None specified",
            input_field_access=input_field_access,
            node_name=info["node_name"],
            prompt=info["prompt"] or "No default prompt provided"
        ))
    
    logger.debug(f"Scaffolded agent: {path}")
    return True


def scaffold_function(
    func_name: str, 
    info: Dict, 
    func_path: Path
) -> bool:
    """
    Create a scaffold file for a function.
    
    Args:
        func_name: Name of function to scaffold
        info: Information about the function
        func_path: Directory to create function module in
        
    Returns:
        True if function was scaffolded, False if it already existed
    """
    file_name = f"{func_name}.py"
    path = func_path / file_name
    
    if path.exists():
        return False
    
    # Generate context fields documentation
    context_fields = generate_context_fields(info["input_fields"], info["output_field"])
    
    # Load template
    template = load_template("function_template")
    
    # Create function file
    with path.open("w") as out:
        out.write(template.format(
            func_name=func_name,
            context_description=info["context"] or "No context description provided",
            context_fields=context_fields,
            success_node=info["success_next"] or "None",
            failure_node=info["failure_next"] or "None",
            node_name=info["node_name"]
        ))
    
    logger.debug(f"Scaffolded function: {path}")
    return True


def scaffold_agents(
    output_dir: Optional[str] = None, 
    func_dir: Optional[str] = None,
    csv_path: Optional[str] = None,
    graph_name: Optional[str] = None,
    config_path: Optional[Union[str, Path]] = None
) -> int:
    """
    Scaffold agents and functions from the CSV.
    
    Args:
        output_dir: Directory to create agent classes in (overrides config)
        func_dir: Directory to create function modules in (overrides config)
        csv_path: Path to CSV file (overrides config)
        graph_name: Optional graph name to filter by
        config_path: Optional path to a custom config file
    
    Returns:
        Number of agents or functions scaffolded
    """
    # Use config system if not explicitly provided
    csv_file = csv_path or get_csv_path(config_path)
    csv_path = Path(csv_file)
    output_path = Path(output_dir) if output_dir else get_custom_agents_path(config_path) 
    func_path = Path(func_dir) if func_dir else get_functions_path(config_path)
    
    # Create directories if they don't exist
    output_path.mkdir(parents=True, exist_ok=True)
    func_path.mkdir(parents=True, exist_ok=True)

    # Collect information about agents and functions
    agent_info = collect_agent_info(csv_path, graph_name)
    func_info = collect_function_info(csv_path, graph_name)
    
    # Scaffold agents
    scaffolded_count = 0
    for agent_type, info in agent_info.items():
        if scaffold_agent(agent_type, info, output_path):
            scaffolded_count += 1
    
    # Scaffold functions
    for func_name, info in func_info.items():
        if scaffold_function(func_name, info, func_path):
            scaffolded_count += 1
    
    return scaffolded_count


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Scaffold agents and functions from CSV")
    parser.add_argument("--csv", help="Path to CSV file")
    parser.add_argument("--graph", help="Graph name to filter by")
    parser.add_argument("--output", help="Directory for agent output")
    parser.add_argument("--functions", help="Directory for function output")
    parser.add_argument("--config", help="Path to custom config file")
    
    args = parser.parse_args()
    
    scaffolded = scaffold_agents(
        csv_path=args.csv,
        graph_name=args.graph,
        output_dir=args.output,
        func_dir=args.functions,
        config_path=args.config
    )
    
    logger.debug(f"Scaffolded {scaffolded} agents/functions")