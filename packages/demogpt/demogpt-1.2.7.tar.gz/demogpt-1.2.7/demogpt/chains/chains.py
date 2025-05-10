import json
import os
import re
from time import sleep

import autopep8
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

from demogpt import utils
from demogpt.chains.task_definitions import getPlanGenHelper, getTasks
from demogpt.controllers import validate

from . import prompts


class Chains:
    @classmethod
    def setLlm(
        cls,
        model,
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        temperature=0.0,
        openai_api_base=None,
        has_gpt4=False
    ):
        cls.openai_api_key=openai_api_key
        cls.temperature=temperature
        cls.openai_api_base=openai_api_base
        cls.has_gpt4=has_gpt4
        cls.llm = ChatOpenAI(
            model=model,
            openai_api_key=openai_api_key,
            temperature=temperature,
            openai_api_base=openai_api_base
        )
        cls.model = model
    
    @classmethod
    def getModel(cls, change=False, temperature=0, change_model="gpt-4-0613"):
        if change and cls.has_gpt4:
            return ChatOpenAI(
                model=change_model,
                openai_api_key=cls.openai_api_key,
                temperature=temperature,
                openai_api_base=cls.openai_api_base
        )
        
        if temperature > 0:
            return ChatOpenAI(
                model=cls.model,
                openai_api_key=cls.openai_api_key,
                temperature=temperature,
                openai_api_base=cls.openai_api_base
        )
        
        return cls.llm
        
    @classmethod
    def setModel(cls, model):
        cls.model = model

    @classmethod
    def getChain(cls, system_template="", human_template="", change=False, change_model="gpt-4-0613", temperature=0, return_type="text", **kwargs):
        prompts = []
        if system_template:
            prompts.append(SystemMessagePromptTemplate.from_template(system_template))
        if human_template:
            prompts.append(HumanMessagePromptTemplate.from_template(human_template))
        chat_prompt = ChatPromptTemplate.from_messages(prompts)
        
        if return_type == "json":
            parser = utils.refine | JsonOutputParser()
        elif return_type == "code":
            parser = utils.refine | StrOutputParser()
        else:
            parser = StrOutputParser()
        
        chain = chat_prompt | cls.getModel(change=change, temperature=temperature, change_model=change_model) | parser
        
        return chain.invoke(kwargs)
    
    @classmethod
    def title(cls, instruction):
        return cls.getChain(
            system_template=prompts.title.system_template,
            human_template=prompts.title.human_template,
            change=False,
            temperature=0.8,
            instruction=instruction
        ).replace('"','').replace("'","")

    @classmethod
    def appType(cls, instruction):
        return cls.getChain(
            system_template=prompts.app_type.system_template,
            human_template=prompts.app_type.human_template,
            change=True,
            instruction=instruction,
            return_type="json"
        )

    @classmethod
    def systemInputs(cls, instruction):
        return cls.getChain(
            system_template=prompts.system_inputs.system_template,
            human_template=prompts.system_inputs.human_template,
            change=False,
            instruction=instruction,
        )

    @classmethod
    def planWithInputs(cls, instruction, system_inputs, app_type):
        TASK_DESCRIPTIONS, TASK_NAMES, TASK_DTYPES = getTasks(app_type)[:3]
        helper = getPlanGenHelper(app_type)
        plan = cls.getChain(
            system_template=prompts.plan_with_inputs.system_template,
            human_template=prompts.plan_with_inputs.human_template,
            change=False,
            instruction=instruction,
            system_inputs=system_inputs,
            helper=helper,
            TASK_DESCRIPTIONS=TASK_DESCRIPTIONS,
            TASK_NAMES=TASK_NAMES,
            TASK_DTYPES=TASK_DTYPES,
        )
        return cls.refinePlan(plan)

    @classmethod
    def planFeedback(cls, instruction, plan):
        return cls.getChain(
            system_template=prompts.plan_feedback.system_template,
            human_template=prompts.plan_feedback.human_template,
            change=False,
            instruction=instruction,
            plan=plan,
            return_type="json"
        )

    @classmethod
    def planRefiner(cls, instruction, plan, feedback, app_type):
        _, TASK_NAMES, _, TASK_PURPOSES = getTasks(app_type)[:4]
        return cls.getChain(
            system_template=prompts.plan_refiner.system_template,
            human_template=prompts.plan_refiner.human_template,
            change=True,
            instruction=instruction,
            plan=plan,
            feedback=feedback,
            TASK_NAMES=TASK_NAMES,
            TASK_PURPOSES=TASK_PURPOSES,
        )

    @classmethod
    def tasks(cls, instruction, plan, app_type):
        TASK_DESCRIPTIONS, TASK_NAMES= getTasks(app_type)[:2]
        
        tasks = cls.getChain(
            system_template=prompts.tasks.system_template,
            human_template=prompts.tasks.human_template,
            instruction=instruction,
            plan=plan,
            TASK_DESCRIPTIONS=TASK_DESCRIPTIONS,
            TASK_NAMES=TASK_NAMES,
            return_type="json"
        )
            
        return utils.reformatTasks(tasks)

    @classmethod
    def taskController(cls, tasks, app_type):
        return validate(tasks, app_type)

    @classmethod
    def planController(cls, plan, app_type):
        return validate(plan, app_type)

    @classmethod
    def refineTasks(cls, instruction, tasks, feedback, app_type):
        _, TASK_NAMES, _, TASK_PURPOSES = getTasks(app_type)[:4]
        
        tasks = cls.getChain(
            system_template=prompts.task_refiner.system_template,
            human_template=prompts.task_refiner.human_template,
            instruction=instruction,
            tasks=tasks,
            feedback=feedback,
            TASK_NAMES=TASK_NAMES,
            TASK_PURPOSES=TASK_PURPOSES,
            return_type="json"
            )
            
        return utils.reformatTasks(tasks)

    @classmethod
    def combine(cls, instruction, code_snippets, plan):
        return cls.getChain(
            system_template=prompts.combine.system_template,
            human_template=prompts.combine.human_template,
            instruction=instruction,
            code_snippets=code_snippets,
            plan=plan,
            return_type="code"
        )
    
    @classmethod
    def howToUse(cls, plan):
        steps = cls.getChain(
            system_template=prompts.how_to_use.system_template,
            human_template=prompts.how_to_use.human_template,
            plan=plan
        )
        
        total_code = f'st.sidebar.markdown("""{steps}""")\n'
        return total_code
    
    @classmethod
    def about(cls, instruction, title):
        markdown = cls.getChain(
            system_template=prompts.about.system_template,
            human_template=prompts.about.human_template,
            instruction=instruction,
            title=title
        )
        
        code = f'\nst.sidebar.markdown("# About")\nst.sidebar.markdown("""{markdown}""")'
        return code

    @classmethod
    def imports(cls, code_snippets):
        return cls.getChain(
            system_template=prompts.imports.system_template,
            human_template=prompts.imports.human_template,
            code_snippets=code_snippets,
            return_type="code"
        )

    @classmethod
    def combine_v2(cls, code_snippets, function_names):
        code = cls.getChain(
            system_template=prompts.combine_v2.system_template,
            human_template=prompts.combine_v2.human_template,
            change=True,
            change_model="gpt-3.5-turbo",
            code_snippets=code_snippets,
            function_names=function_names,
            return_type="code"
        )
        
        code = autopep8.fix_code(code)
        
        has_problem = utils.catchErrors(code)
        
        if has_problem:
            print("Switching to the 16k...")
            code = cls.getChain(
                system_template=prompts.combine_v2.system_template,
                human_template=prompts.combine_v2.human_template,
                change=True,
                change_model="gpt-3.5-turbo-16k-0613",
                code_snippets=code_snippets,
                function_names=function_names,
                return_type="code"
            )
        
        return code

    @classmethod
    def feedback(cls, instruction, code):
        return cls.getChain(
            system_template=prompts.feedback.system_template,
            human_template=prompts.feedback.human_template,
            instruction=instruction,
            code=code,
        )

    @classmethod
    def refinePlan(cls, plan):
        pattern = r"\[[a-zA-Z0-9_]+\(.*\)"
        steps = plan.strip().split("\n")
        refined_plan = []
        index = 1
        for i in range(len(steps)):
            step = steps[i]
            # If current step contains the pattern or next step contains the pattern, then retain
            if re.search(pattern, step):
                # Remove existing numbering
                current_step = re.sub(r"^\d+\.", "", step).strip()
                refined_plan.append(f"{index}. {current_step}")
                index += 1
        return "\n".join(refined_plan)
    
    @classmethod
    def addAboutAndHTU(cls, instruction, title, code_snippets, plan):
        sleep(1)
        how_to_markdown = cls.howToUse(plan=plan)
        sleep(2)
        about = cls.about(instruction=instruction, title=title)
        pattern = r'(openai_api_key\s*=\s*st\.sidebar\.text_input\((?:[^()]*|\([^)]*\))*\))'
        # replacement string with additional code
        replacement = how_to_markdown + r'\1' + about
        # substitute using regex
        final_code = re.sub(pattern, replacement, code_snippets, flags=re.DOTALL)
        return final_code
    
    @classmethod
    def getAboutAndHTU(cls, instruction, title, plan):
        sleep(1)
        how_to = cls.howToUse(plan=plan)
        sleep(2)
        about = cls.about(instruction=instruction, title=title)
        return how_to, about 

    @classmethod
    def refine(cls, instruction, code, feedback):
        return cls.getChain(
            system_template=prompts.refine.system_template,
            human_template=prompts.refine.human_template,
            instruction=instruction,
            code=code,
            feedback=feedback,
            return_type="code"
        )

    @classmethod
    def final(cls, draft_code):
        return cls.getChain(
            system_template=prompts.final.system_template,
            human_template=prompts.final.human_template,
            draft_code=draft_code,
            return_type="code"
        )