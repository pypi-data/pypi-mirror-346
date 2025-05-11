def chunks(data, n: int = 2):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(data), n):
        yield data[i:i + n]
