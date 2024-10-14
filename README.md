# LLM Tokenizer using BPE

This project implements a tokenizer for a Large Language Model (LLM) using Byte-Pair Encoding (BPE). The tokenizer is designed to preprocess textual data by converting it into a form that is suitable for language model training and inference, efficiently splitting the text into subword tokens.

## Project Structure

```bash
├── saved_models/             # Directory for saving trained tokenizer (merges, vocabulary)
├── training_dataset/         # Directory for storing training datasets
├── main.ipynb                # Jupyter notebook for running the tokenizer and experimenting with data
├── pdf_to_text.py            # Script for converting PDF documents into plain text
├── tokenizer.py              # BPE tokenizer --> Encodes and decodes text
├── train_bpe_tokenizer.py    # Script to train the BPE tokenizer on a dataset
├── utility.py                # Utility functions used across the project
```

## Features

- **BPE Tokenization**: Tokenizes input text using Byte-Pair Encoding, which is highly effective for compressing vocabularies and handling rare words.
- **PDF Conversion**: Includes functionality to convert PDF files to plain text for easier processing.
- **Training on Custom Data**: Allows training a BPE tokenizer on a custom dataset.
- **Saving and Loading Models**: You can save and load trained tokenizers for later use in inference or fine-tuning.

## Installation

To use this project, you will need the following dependencies:

```bash
pip install PyPDF2 regex
```

## Usage

1. **Train the BPE Tokenizer**:

   Use the `train_bpe_tokenizer.py` script to train the BPE tokenizer on your custom dataset.

2. **Convert PDF to Text**:

   If you have data in PDF format, convert it to plain text using `pdf_to_text.py`.

3. **Experiment with the Tokenizer**:

   Open the `main.ipynb` notebook to explore how the tokenizer works and run experiments on sample text or datasets.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the project.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
