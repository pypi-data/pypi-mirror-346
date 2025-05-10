from typing import AsyncIterator, Iterator, List

from pinaxai.document import Document
from pinaxai.document.reader.csv_reader import CSVUrlReader
from pinaxai.knowledge.agent import AgentKnowledge
from pinaxai.utils.log import logger


class CSVUrlKnowledgeBase(AgentKnowledge):
    urls: List[str]
    reader: CSVUrlReader = CSVUrlReader()

    @property
    def document_lists(self) -> Iterator[List[Document]]:
        for url in self.urls:
            if url.endswith(".csv"):
                yield self.reader.read(url=url)
            else:
                logger.error(f"Unsupported URL: {url}")

    @property
    async def async_document_lists(self) -> AsyncIterator[List[Document]]:
        for url in self.urls:
            if url.endswith(".csv"):
                yield await self.reader.async_read(url=url)
            else:
                logger.error(f"Unsupported URL: {url}")
