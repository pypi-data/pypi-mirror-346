class DataAnalysis:
  @staticmethod
  def split(x, y, split):
    split_index = int(len(x) * split)
    return x[:split_index], x[split_index:], y[:split_index], y[split_index:]

  @staticmethod
  def normalize(x):
    x = np.array(x)
    mean = np.mean(x)
    std = np.std(x)
    return (x - mean) / std
