import numpy as np
import pandas as pd

import esm
import torch
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


from Bio import SeqIO
#from google.colab import drive
#drive.mount('/content/drive')

def load_fasta_sequences(fasta_path):
    """Reads sequences from a FASTA file and returns a list of (label, sequence) tuples."""
    return [(record.id, str(record.seq)) for record in SeqIO.parse(fasta_path, "fasta")]

import os

def load_fasta_sequences_from_folder(folder_path):
    """Reads one sequence per FASTA file and returns a list of (filename, sequence) tuples."""
    sequences = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".fasta") or filename.endswith(".fa"):
            path = os.path.join(folder_path, filename)
            records = list(SeqIO.parse(path, "fasta"))
            if records:  # In case the file is not empty
                sequences.append((filename, str(records[0].seq)))

    return sequences

def extract_embeddings(sequences: list) -> np.array:
    """Extract the embedded 1280-dim 'dense' vector from the provided sequences"""
    print(sequences)
    model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
    batch_converter = alphabet.get_batch_converter()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    batch_labels, batch_strs, batch_tokens = batch_converter(sequences)
    batch_tokens = batch_tokens.to(device)

    # Run the model to get representations from the final layer (layer 33)
    with torch.no_grad():
        results = model(batch_tokens, repr_layers=[33], return_contacts=False)

    # Get per-residue embeddings
    token_embeddings = results["representations"][33]  # Shape: (batch_size, seq_length, embedding_dim)

    # Get per-sequence embedding (mean-pooled)
    sequence_embedding = token_embeddings.mean(dim=1)

    return sequence_embedding

def reduce_emeddings(dim_red:str, embeddings:pd.DataFrame, n_components=2, perplexity=10, random_state=42):
    """
    Reduce high-dimensional embeddings using custom dimension reduction technique.

    Parameters:
    - embeddings: np.ndarray of shape (n_samples, n_features)
    - n_components: int, dimension of the reduced space (2 or 3)
    - perplexity: int, t-SNE perplexity (default: 30)
    - random_state: int, ensures reproducibility

    Returns:
    - reduced_embeddings: np.ndarray of shape (n_samples, n_components)
    """
    reduced_embeddings = None
    if dim_red == 'tSNE':
      tsne = TSNE(n_components=n_components, perplexity=perplexity, random_state=random_state)
      reduced_embeddings = tsne.fit_transform(embeddings)
      return reduced_embeddings
    elif dim_red == 'PCA':
      PCA = PCA(n_components=n_components)
      reduced_embeddings = PCA.fit_transform(embeddings)
      return reduced_embeddings
    else:
      print('wrong dim_red, terminating')



def plot_embeddings(dim_red:str, reduced_embeddings: pd.DataFrame, labels: list=None) -> None:
    """
    Plot 2D t-SNE embeddings using Matplotlib.

    Parameters:
    - reduced_embeddings: np.ndarray of shape (n_samples, 2)
    - labels: List or np.ndarray of shape (n_samples,) for coloring points (optional)
    - title: str, title of the plot
    """
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c=labels, cmap="viridis", alpha=0.7)
    plt.colorbar(scatter, label="Labels" if labels is not None else "Color Scale")
    plt.title('Reduced Embeddings using ')
    plt.xlabel(f"{dim_red} Component 1")
    plt.ylabel(f"{dim_red} Component 2")
    plt.show()

def pipeline(filename: str, dim_red_method: str='tSNE'):
  my_seqs = load_fasta_sequences(filename)
  embeddings = extract_embeddings(sequences=my_seqs)
  # Move to CPU and convert to numpy
  embeddings_np = embeddings.cpu().numpy()

  reduced_embeddings = reduce_emeddings(dim_red=dim_red_method, embeddings=embeddings_np, )
  plot_embeddings(dim_red=dim_red_method, reduced_embeddings=reduced_embeddings)

# pipeline(my_seqs=my_seqs, dim_red_method='tSNE')

