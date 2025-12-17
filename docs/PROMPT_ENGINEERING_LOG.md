## Session Date: December 13, 2025

### Prompt 1
```
we have a new assignment. i am attaching it so you can read it and then we will starts step after step.
file attached
```

---

### Prompt 2
```
first  we ahpuld build the repo . and  for every file you create output an actual file
```

---

### Prompt 3
```
I added ARCHITECTURE.md and generator.py
```

---

### Prompt 4
```
/Users/ofrikutchinsky/miniconda3/envs/prompt-engineering-project/bin/python /Users/ofrikutchinsky/Documents/prompt-engineering-project/src/try_evaluator.py Total predictions: 9 Correct predictions: 6 Accuracy: 0.667
```

---

### Prompt 5
```
i built a new pytho 3.11 env. now CoT experiment ran and CSVs were created
```

---

### Prompt 6
```
/Users/ofrikutchinsky/miniconda3/envs/prompt-engineering-project/bin/python /Users/ofrikutchinsky/Documents/prompt-engineering-project/src/try_config.py Traceback (most recent call last): File "/Users/ofrikutchinsky/Documents/prompt-engineering-project/src/try_config.py", line 20, in <module> main() File "/Users/ofrikutchinsky/Documents/prompt-engineering-project/src/try_config.py", line 5, in main cfg = load_config() ^^^^^^^^^^^^^ File "/Users/ofrikutchinsky/Documents/prompt-engineering-project/src/prompt_lab/config/loader.py", line 69, in load_config raise FileNotFoundError(f"Config file not found: {path}") FileNotFoundError: Config file not found: /Users/ofrikutchinsky/Documents/prompt-engineering-project/src/config/default.yaml
```

---

### Prompt 7
```
Dummy LLM client works, Connect methods to the LLM client
```

---

### Prompt 8
```
(prompt-engineering-project) ofrikutchinsky@ofris-MBP prompt-engineering-project % pytest ======================================================================================================= test session starts ======================================================================================================= platform darwin -- Python 3.11.14, pytest-9.0.2, pluggy-1.6.0 rootdir: /Users/ofrikutchinsky/Documents/prompt-engineering-project configfile: pyproject.toml plugins: cov-7.0.0 collected 4 items tests/test_dataset.py .. [ 50%] tests/test_metrics.py .. [100%] ======================================================================================================== 4 passed in 0.01s ========================================================================================================
```

---
### Prompt 9
```
it works but answers are still dummy answer is that ok ?
```

---
### Prompt 10
```
lets connect now to real LLMclient and focus on these two methods
```

---
### Prompt 11
```
ok we have a problem at the moment to get a key so we will continue with dummy until this resolves
```

---
### Prompt 12
```
i want to work now on adding the openai API connection. in prior assignment we had to use it as well and my partner built these files attached. 
```

---
### Prompt 13
```
this is the azure_openai_helper.llm_client.py. we also didnt write anything that connects it to utils.llm_client.py
```

---
### Prompt 14
```
ok but we do want to connect to a azure_opanai. we have a key. we started this step of connecting to actual llm through azure opanai API
```

---
### Prompt 15
```
ok i will have that in a moment. can we work now on next steps? how do we want to build an expriment? how do we want to show the results
```

---
### Prompt 16
```
i want to write data analysis scripts now. we would want to show the following results- 1. syntax changes in prompt vs accuracy - in each of the methods separately and maybe think of a matrix to evaluate "how much these changes effect the accuracy of the method" 2. run same prompt in all method and compare accuracies 3. any other research questions you think are interesting
```

---
### Prompt 17
```
im debating whether to have each suitable analysis script output a plot as .jpg or table as .csv OR each to create a html report with all relevant visualisations
```

---
### Prompt 18
```
can we have an option to run all methods experiments at once?
```

### Prompt 19
```
it has a problem with run_fewshot_experiment. --- Running fewshot experiment: /Users/ofrikutchinsky/Documents/prompt-engineering-project/src/run_fewshot_experiment.py --- Traceback (most recent call last): File "/Users/ofrikutchinsky/Documents/prompt-engineering-project/src/run_fewshot_experiment.py", line 13, in <module> from prompt_lab.utils.llm_client import DummyLLMClient, OpenAILLMClient ImportError: cannot import name 'OpenAILLMClient' from 'prompt_lab.utils.llm_client' (/Users/ofrikutchinsky/Documents/prompt-engineering-project/src/prompt_lab/utils/llm_client.py) [ERROR] Experiment for method 'fewshot' failed with exit code 1.
```

---

### Prompt 20
```
ok i moved analysis to scr. should i leave the init empty?
```

---

### Prompt 21
```
can we somehow check in "run_baseline_expriment"? because while debugging it seems like it is using the actual api and not dummy
```

---

### Prompt 22
```
thing here that even though we explicitly asks the agent for one word answer it still sometimes return more than that. we consider it a wrong answer regardeless of the content of the answer because it is either way not what we asked for. where is this written ? this shouldnt be.
```

---

### Prompt 23
```
geat. so in term of experminets we are good? we need to work just on resuts- research and technical issues?
```

---
### Prompt 24
```
the README should have two parts: 1. first, a regular readme as we know it. the whole project is supposed to act as a pyhton package that one can run. so we need a whole detialed description of how to use this package- we want to the user to be able to set "dummy" or "azure" we want him to be able to give a jason file for himself (this also requires a change in the config" and he needs to get his own azure Openai key in his env file. 2. second will be the report of our results he wants. lets work part by part
```

---
### Prompt 25
```
but do we have the utilities to run this package from a terminal with parameters? i think we still need to make some minor changes to package this project
```

---
### Prompt 26
```
and if the user wants to import it to a script like a library is it possible?
```

---
### Prompt 27
```
i cant copy paste this.. i want a file i can download. i am also attaching the report because i will need to add figuers and interpataions. if you can add an actual image use a place holder and i will ad it
```

---
### Prompt 28
```
i need the readme longer, more detailed because thats what he wants. what more can we say about the project? we want to add that dummy option is for debuginf seeing the instaltion works regardless of venv installation anything else?
```

### Prompt 29
```
ok next step is to give you the full project again and the file that specified what we need and see if we have it all. 
```

---


