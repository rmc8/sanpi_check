from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class Sanpi:
    def __init__(self, llm: ChatOllama):
        self.llm = llm

    @staticmethod
    def _get_sanpi_template(system_massages: str) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", system_massages),
                ("human", "{query}"),
            ]
        )

    def _get_agreement_template(self) -> ChatPromptTemplate:
        return self._get_sanpi_template(
            system_massages="あなたは賛成意見を積極的に述べます。著しい問題が無い場合、ユーザーの意見を洗練させるために、質問に大してなるべく具体的に明確で賛同的な意見を述べてください。"
        )

    def _get_disagreement_template(self) -> ChatPromptTemplate:
        return self._get_sanpi_template(
            system_massages="あなたは反対意見を積極的に述べます。反対する余地がある場合、ユーザーの意見を洗練させるために、質問に大してなるべく具体的に明確で反対的な意見を述べてください。"
        )

    def run(self, query: str) -> str:
        # 賛成意見の処理
        agreement_chain = self._get_agreement_template() | self.llm | StrOutputParser()
        # 反対意見の処理
        disagreement_chain = (
            self._get_disagreement_template() | self.llm | StrOutputParser()
        )
        # 賛否の集約処理
        parallel_chain = RunnableParallel(
            {
                "agree": agreement_chain,
                "disagree": disagreement_chain,
            }
        )
        summarize_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたは意見の善し悪しを素直に見極められる達観したAIです。賛否の意見を適切にまとめてください。まとめはナラティブ形式で自然にお願いします。",
                ),
                ("human", "賛成意見： {agree}\n\n反対意見: {disagree}"),
            ]
        )
        summarize_chain = (
            parallel_chain | summarize_prompt | self.llm | StrOutputParser()
        )
        final_output = summarize_chain.invoke({"query": query})
        return final_output
