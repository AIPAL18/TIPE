from rolling_hash import RollingHash

if __name__ == "__main__":
    try:
        assert 1 == 0, "normal"
    except AssertionError:
        print("ok")
    
    hasher = RollingHash()
    assert hasher.hash("abc") == 6432038, "test 1"
    assert hasher.hash("bcd") == 6498345, "test 2"

    hasher = RollingHash()
    h = hasher.hash("abc")
    new_h = hasher.next_hash("d")
    assert new_h == RollingHash().hash("bcd"), "test 3"
