# Obsidian LLM Vault Folder Structure

## Model Vault Folder Struture

```
├── Agents/
│ └── CustomGPT1.md
├── Prompts/
│ ├── General/
│ └── Specific/
├── Outputs/
│ ├── Raw/
│ └── Processed/
├── Context/
│ ├── Background/
│ └── CurrentState/
├── Metadata/
│ ├── Tags/
│ └── Categories/
└── Templates/
├── AgentTemplates/
└── PromptTemplates/
```


---


## Folder Descriptions

### Agents
Contains configurations and definitions for different LLM agents.
- **CustomGPT1.md**: Example agent configuration file

### Prompts
Stores various prompts used in LLM interactions.
- **General**: Common, multi-purpose prompts
- **Specific**: Prompts tailored for particular tasks or domains

### Outputs
Contains the results and outputs from LLM interactions.
- **Raw**: Unprocessed outputs directly from the LLM
- **Processed**: Refined or analyzed versions of the raw outputs

### Context
Stores contextual information for LLM interactions.
- **Background**: Long-term, stable context information
- **CurrentState**: Dynamic, session-specific context

### Metadata
Holds metadata for organizing and categorizing vault contents.
- **Tags**: Collection of tags used across the vault
- **Categories**: Broader categories for classifying content

### Templates
Houses reusable templates for agents and prompts.
- **AgentTemplates**: Boilerplate structures for creating new agents
- **PromptTemplates**: Reusable prompt structures for different scenarios