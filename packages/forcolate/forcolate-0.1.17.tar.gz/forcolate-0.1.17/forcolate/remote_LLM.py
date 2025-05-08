import requests
import json
from smolagents import ToolCollection, CodeAgent
from mcp import StdioServerParameters
import os
from smolagents import ActionStep, TaskStep
from smolagents import OpenAIServerModel

# These functions are not injected directly in the default set of tools because they use remote servers with specific API keys
# and are not open source. They are provided as examples of how to use the tools.



def get_LLM_response(query, folder_in="", folder_out=""):

  # get the url, model and key from a config file

  config_file = "config.json"
  with open(config_file, 'r') as f:
    config = json.load(f)
    url = config["LLMurl"]
    model = config["LLMmodel"]
    key = config["LLMkey"]

  # example of the config file
  # {
  #   "LLMurl": "https://openrouter.ai/api/v1/chat/completions",
  #   "LLMmodel": "qwen/qwen3-4b:free",
  #   "LLMkey": "your_api_key"
  # }

  # check if the url, model and key are not empty       
    if not url or not model or not key:
        raise ValueError("Please provide a valid url, model and key in the config file")


  # read all files in the folder_in directory
  prompt_and_query = "Answer the question based on the context below : \n QUESTION: " + query + "\n"

  context = "Below is the context from the files in the folder:\n CONTEXT: " 
  if folder_in:
    import os
    for filename in os.listdir(folder_in):
      if filename.endswith(".txt") or filename.endswith(".md"):
        with open(os.path.join(folder_in, filename), 'r') as f:
          context += f.read() + "\n"
 
  # Combine the context and query
  context_and_query = prompt_and_query + context
 
  response = requests.post(
    url=url,
    headers={
      "Authorization": "Bearer " + key,
    },
    data=json.dumps({
      "model": model,
      "messages": [
        {
          "role": "user",
          "content": context_and_query
        }
      ]
    })
  )

  response_json = response.json()['choices'][0]['message']['content']

  # Save the response to a file
  if folder_out:
    with open(f"{folder_out}/answer.md", "w") as f:
      f.write(response_json)

  return response_json



def run_agent(agent, query, folder_in ="", folder_out=""):
    
    
    agent.python_executor.send_tools({**agent.tools})

    # Run the agent with the task
    agent.memory.steps.append(TaskStep(task=query, task_images=[]))
    final_answer = None
    step_number = 1
    while final_answer is None and step_number <= 10:
        memory_step = ActionStep(
            step_number=step_number,
            observations_images=[],
        )
        # Run one step.
        final_answer = agent.step(memory_step)
        agent.memory.steps.append(memory_step)
        
        # Save the memory to a file
        with open(f"{folder_out}/step_{step_number}_thought_process.json", "w") as f:
            f.write(memory_step.model_output_message.model_dump_json())
        with open(f"{folder_out}/step_{step_number}_observation.md", "w") as f:
            f.write(memory_step.observations)
            
        step_number += 1

    if final_answer:
        with open(f"{folder_out}/answer.md", "w") as f:
            f.write(f"{final_answer}")

    return f"{final_answer}"

def get_LLM_agent_response(query, folder_in="", folder_out=""):


  server_parameters = None
  config_file = "config.json"
  with open(config_file, 'r') as f:
    config = json.load(f)
    url = config["LLMurl"]
    # remove everythin after the v1 tag
    url = url.split("v1")[0] + "v1"
    modelname = config["LLMmodel"]
    key = config["LLMkey"]

    if "MCPcommand" in config:
      MCPcommand = config["MCPcommand"]
      MCPargs = config["MCPargs"]
      # transform MCPargs into a list
      MCPargs = MCPargs.split(" ")
      MCPenv = config["MCPenv"]
      # transform MCPenv into a dict
      MCPenv = dict(item.split("=") for item in MCPenv.split(","))
      # add MCPenv to the env of the StdioServerParameters
      MCPenv = {**MCPenv, **os.environ}

      server_parameters = StdioServerParameters(
          command=MCPcommand,
          args=MCPargs,
          env=MCPenv,
      )


  model = OpenAIServerModel(
      model_id=modelname,
      api_base=url,
      api_key=key,
  )
  if server_parameters:
    with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as tool_collection:
        
        agent = CodeAgent(tools=[*tool_collection.tools], model=model, verbosity_level=1, add_base_tools=True)
        return run_agent(agent, query, folder_in, folder_out)
  else:
    agent = CodeAgent(tools=[],model=model, verbosity_level=1, add_base_tools=True)
    return run_agent(agent, query, folder_in, folder_out) 
  

def get_list_of_MCP_tools():
  # get the list of tools from the MCP server
  new_tools = []


  config_file = "config.json"
  with open(config_file, 'r') as f:
    config = json.load(f)
    if "MCPcommand" in config:
      MCPcommand = config["MCPcommand"]
      MCPargs = config["MCPargs"]
      # transform MCPargs into a list
      MCPargs = MCPargs.split(" ")
      MCPenv = config["MCPenv"]
      # transform MCPenv into a dict
      MCPenv = dict(item.split("=") for item in MCPenv.split(","))
      # add MCPenv to the env of the StdioServerParameters
      MCPenv = {**MCPenv, **os.environ}

      server_parameters = StdioServerParameters(
          command=MCPcommand,
          args=MCPargs,
          env=MCPenv,
      )

    with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as tool_collection:
        # get the list of tools from the MCP server
        for tool in tool_collection.tools:
            new_tools.append((tool.name, tool.description, lambda q,fin,fout  : get_LLM_agent_response(q+f"/n use tool {tool.name}",fin,fout)))

  return new_tools


LLM_TOOLS = [(
    "Ask LLM",
    "Ask LLM : this tool will ask the LLM to answer the question based on the context provided in the folder directory",
    get_LLM_response
),(
  "Ask LLM Agent",
  "Ask LLM Agent : this tool will ask the LLM to answer the question based on the context provided in the folder directory and will use an agent and tools in MCP to do so",
  get_LLM_agent_response
)]
