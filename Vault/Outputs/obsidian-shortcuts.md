# Prompt

When I'm capturing LLM interactions in Obsidian, I type a lot of the same things. An example is typing #Prompt and #Output to divide up the page. Let's think of ways to automate this. Can you suggest some hotkeys and ways that I can use template plugins to cut down on this manual data entry? As you know, one conversation with an LLM can include many prompts and outputs so some way to automate the incrementing process (ie, 'Prompt 2', 'Output 2') would be especially helpful.

# Output

Based on the information provided in the search results and your specific needs for capturing LLM interactions, here are some suggestions to automate and streamline your process using Obsidian plugins and hotkeys:

1. Hotkeys for Templates Plugin:
   This plugin allows you to set up hotkeys for specific templates[1]. You can create templates for your common structures (like #Prompt and #Output) and assign hotkeys to them.

   - Create templates for "Prompt" and "Output" sections
   - Set up hotkeys for each template in the plugin settings
   - Use these hotkeys to quickly insert the structured sections

2. Templater Plugin:
   Templater is more powerful and flexible than the core Templates plugin[2]. It allows for dynamic content and can be bound to hotkeys.

   - Create a template that includes both #Prompt and #Output sections
   - Use Templater's scripting capabilities to increment numbers automatically
   - Bind this template to a hotkey for quick insertion

3. QuickAdd Plugin:
   This plugin can be used to create custom commands and menus[4].

   - Set up a QuickAdd command to insert your structured prompts and outputs
   - Create a multi-menu for different types of insertions (e.g., new prompt, new output, both)
   - Assign a hotkey or mobile swipe action to trigger this menu

4. Incremental ID Plugin:
   While not directly related to prompts and outputs, this plugin can help with automatic numbering[3].

   - Set up prefixes for prompts and outputs (e.g., "P" for prompts, "O" for outputs)
   - Use the plugin's templater code to automatically insert and increment IDs

5. Mobile Hotbar Customization:
   For mobile use, customize the hotbar to include your most frequently used commands[4].

   - Add commands for inserting prompts, outputs, or both
   - Arrange these for easy access on your mobile device

6. Text Expansion:
   Consider using a system-wide text expander like Espanso (mentioned in [2]) for quick insertion of common phrases or structures.

Implementation steps:

1. Create templates for your common structures (Prompt and Output sections).
2. Set up the Hotkeys for Templates plugin or Templater to assign hotkeys to these templates.
3. Use QuickAdd to create a menu or command for inserting these structures, with options for incrementing numbers.
4. Customize your mobile hotbar with these commands for easy access on mobile devices.
5. Consider using the Incremental ID plugin for automatic numbering of prompts and outputs.

By combining these methods, you can significantly reduce manual data entry and streamline your process of capturing LLM interactions in Obsidian. The key is to set up a system that allows for quick insertion of structured content and automatic incrementing of numbers for multiple prompts and outputs within a single conversation.