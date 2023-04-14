def test_ingest(ingest_data):
    data = ingest_data

    assert data.shape == (73268, 79)
