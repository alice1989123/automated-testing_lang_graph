from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser


def parser (code_dir ):
    loader = GenericLoader.from_filesystem(
        code_dir,
        glob="**/*",
        suffixes=[".py"],
        parser=LanguageParser()
    )
    docs = loader.load()


    d_sorted = sorted(docs, key=lambda x: x.metadata["source"])
    d_reversed = list(reversed(d_sorted))
    concatenated_content = "\n\n\n --- \n\n\n".join(
        [doc.page_content for doc in d_reversed]
    )
    return concatenated_content
