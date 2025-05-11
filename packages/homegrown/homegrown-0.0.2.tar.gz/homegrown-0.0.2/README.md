
# Native 
Agentic workflows uses 2 steps

1. Agent loops: which handles core operation of taking an input and giving an output in micro level. 

2. Agentic Core Components:  peripherals for agentic workflows which enhances agentic workflow into a system level. and give them actual useful problem solving capabilities 


Agent loop consists of core internal flow :

intent  →  plan  →  act  →  interpret  → loop reflection - >  memory ↺

And Agentic Core Components are abstarct features such like:  Multilayer Context
Reflection
Extensive Planning       
Tool Orchestration
Self-Modeling 
Dynamic Memory
Integrated Awareness
Holistic Memory
Autonomous Productive Capacity


there are different approaches to achive/reach these Core Components. And all frameworks treats LLM operations as not enough and support and fill between the operations with lots of python code. 

This has 2 harmful outcomes.  First is scalability problems. To scale your agent you should enhance both agent loop codes and your code resposible of creating abstarct features. Which is not maintainable on the long run. 

Second harmful outcome is about chaining and self calling and recursive looping.  Such manual code based scaffolding makes chaining and self calling non-native and tool calling like.  

So with Native what we do is like every organ in the body is composed of cells and cells are made from atoms, we maintain similar structure in the overall agent by composing each piece from LLMs.  
Agent loop components (intent,  plan ,  act ,  interpret , loop reflection ) are all composed of LLM calls. We dont use python scaffold around everything and this is amazing. 



our framework has 2 slogans

- minimal glue code, maximal LLM calls
- When GLue is absolutely needed, we also use an LLM for glueing

