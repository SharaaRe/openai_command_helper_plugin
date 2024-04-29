import openai 
from dotenv import load_dotenv, find_dotenv
import os
import sys

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.schema import StrOutputParser

from langchain.vectorstores.chroma import Chroma

from langchain.schema.vectorstore import VectorStoreRetriever


from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser




# Specify the path to your .env file
env_file_path = '.env'  # Update this with the correct path

source_path = __file__

# Get the directory of the current file
source_dir = os.path.dirname(source_path)

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']
db = Chroma(
    persist_directory=source_dir + "/chroma",
    embedding_function=OpenAIEmbeddings(model="text-embedding-ada-002"),
)



def load_prompt(prompt_file):

        with open(prompt_file, 'r') as file:
                prompt = file.read().replace('\n', '')
                return prompt
        


doc_prompt = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)

def no_context(user_instruction, model):
    parser = JsonOutputParser()
    template_string = load_prompt(source_dir+'/Project/prompts/9_4.txt')
    prompt = PromptTemplate(
    template=template_string,
    input_variables=["user_instructions"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

    chain = prompt | model | parser

    result = chain.invoke({'user_instruction':user_instruction})
    print(result['RhinoScript'][0])



def with_context(user_instruction, model):


        parser = JsonOutputParser()
        response_schemas = [
            ResponseSchema(name="RhinoScript", description="the runnable script for Rhino3d CLI"),
            ResponseSchema(
                name="description",
                description="The description for the script and the parameters",
            ),
        ]
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        template_string = load_prompt(source_dir+'/Project/prompts/10.txt')

        command_question_template = """You are an expert rhino3d designer who can work with rhino3d  command line api.
            Based on the user instruction, what is the top 2 best RhinoScript "command line" command that can be used to complete this request in three Command keys?
            And what shape better describes the request in one word?
            {input}
        """
        context_prompt = PromptTemplate(
        template=command_question_template,
        input_variables=["context", "input"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        retriever: VectorStoreRetriever = db.as_retriever(search_kwargs={'k': 3})
        context_chain = context_prompt | model | StrOutputParser()
        context_result = context_chain.invoke({'input': user_instruction})
        docs = {"context": retriever.get_relevant_documents(context_result)}

        command_prompt = PromptTemplate(
        template=template_string,
        input_variables=["input"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        retrieval_chain_2 = command_prompt | model | output_parser
        result_2 =retrieval_chain_2.invoke({'input': user_instruction, 'context': docs})
        print(result_2['RhinoScript'][0])



if __name__ == '__main__':
    try:

        user_instruction = sys.argv[1]
        llm_model = "gpt-3.5-turbo" if len(sys.argv) < 3 else sys.argv[2]
        model = ChatOpenAI(temperature=0.0, model=llm_model)
        with_context(user_instruction, model)

    except Exception as e:
        print('ERROR', e)
