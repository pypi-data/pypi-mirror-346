import os
import tempfile
import time

import pytest

from kv_cache import KVStore


@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    yield path
    os.unlink(path)


def test_basic_operations(temp_db):
    store = KVStore(temp_db)
    
    # Test set and get
    store.set("test_key", "test_value")
    assert store.get("test_key") == "test_value"
    
    # Test default value
    assert store.get("nonexistent_key", "default") == "default"
    
    # Test delete
    store.delete("test_key")
    assert store.get("test_key") is None


def test_ttl(temp_db):
    store = KVStore(temp_db)
    
    # Set with 1 second TTL
    store.set("ttl_key", "ttl_value", ttl=1)
    assert store.get("ttl_key") == "ttl_value"
    
    # Wait for expiration
    time.sleep(1.1)
    assert store.get("ttl_key") is None


def test_complex_values(temp_db):
    store = KVStore(temp_db)
    
    # Test dict
    dict_value = {"name": "test", "data": [1, 2, 3]}
    store.set("dict_key", dict_value)
    assert store.get("dict_key") == dict_value
    
    # Test list
    list_value = [1, "test", {"nested": True}]
    store.set("list_key", list_value)
    assert store.get("list_key") == list_value


def test_context_manager(temp_db):
    with KVStore(temp_db) as store:
        store.set("test_key", "test_value")
        assert store.get("test_key") == "test_value"
    
    # Verify the connection is closed
    assert store._conn is None


def test_clear(temp_db):
    store = KVStore(temp_db)
    
    # Add multiple entries
    store.set("key1", "value1")
    store.set("key2", "value2")
    
    # Clear all entries
    store.clear()
    
    # Verify all entries are removed
    assert store.get("key1") is None
    assert store.get("key2") is None

    