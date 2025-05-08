from rara_tools.normalizers.viaf import VIAFRecord, VIAFClient


def test_fetch_clusters_by_id_list():
    viaf_ids = ["7432247", "456"]
    client = VIAFClient()
    
    results = client.fetch_viaf_clusters(viaf_ids)
    assert len(results) == 2
    assert results["456"] == {}
    assert len(results["7432247"]) > 0
    
    
def test_fetch_viaf_results_for_normalizer():
    viaf_ids = ["7432247", "456"]
    client = VIAFClient()
    
    results = client.get_normalized_data(viaf_ids)
    assert len(results) == 2