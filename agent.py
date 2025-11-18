from tools.pdf_reader import extract_pages
from tools.pdf_indexer import PDFIndexer
from tools.search_engine import clean_text, simplify


class PDFAnswerAgent:
    def __init__(self):
        self.indexer = PDFIndexer()
        self.loaded = False

    def load_pdf(self, path):
        pages = extract_pages(path)
        self.indexer.build(pages)
        self.loaded = True
        print("PDF loaded and indexed successfully.")

    def ask(self, question):
        if not self.loaded:
            return "Please load a PDF first using load_pdf()."

        results = self.indexer.search(question, top_k=3)

        if not results:
            return "Couldn't find anything."

        best = results[0]

        real = clean_text(best["text"])
        simple = simplify(real)

        return {
            "page": best["page"],
            "real_answer": real,
            "easy_answer": simple
        }


if __name__ == "__main__":
    agent = PDFAnswerAgent()
    agent.load_pdf("book.pdf") #pdf file name

    while True:
        q = input("\nAsk something: ")
        ans = agent.ask(q)
        print("\nPage:", ans["page"])
        print("\nReal answer:\n", ans["real_answer"])
        print("\n", ans["easy_answer"])
