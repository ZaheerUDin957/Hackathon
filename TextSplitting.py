# TextSplitting.py
class TextSplitter:
    @staticmethod
    def split_text(data):
        return "Text split successfully!"

class CharacterTextSplitter:
    def __init__(self, separator, chunk_size, chunk_overlap, length_function, **kwargs):
        self.separator = separator
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.length_function = length_function
        # Add any other initialization code here...

    def create_documents(self, texts):
        # Add your implementation here...
        # Placeholder logic, modify based on your requirements
        if not texts:
            return []

        splitted_text = []
        for text in texts:
            start = 0
            while start < len(text):
                end = start + self.chunk_size
                chunk = text[start:end]
                splitted_text.append(chunk + self.separator)
                start = end - self.chunk_overlap

            # Remove the last added separator
            splitted_text[-1] = splitted_text[-1].rstrip(self.separator)

        return splitted_text


class RecursiveCharacterTextSplitter:
    def __init__(self, chunk_size, chunk_overlap, length_function, **kwargs):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.length_function = length_function
        # Add any other initialization code here...

    def create_documents(self, texts):
        # Add your implementation here...
        # Placeholder logic, modify based on your requirements
        if not texts:
            return []

        splitted_text = []
        for text in texts:
            start = 0
            while start < len(text):
                end = start + self.chunk_size
                chunk = text[start:end]
                splitted_text.append(chunk)
                start = end - self.chunk_overlap

        return splitted_text
