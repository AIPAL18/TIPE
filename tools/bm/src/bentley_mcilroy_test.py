from bentley_mcilroy import *

if __name__ == "__main__":
    codec = BentleyMcIlroy.Codec
    string = "aaaaaaaaaaaaaaaaaaaaaaa"

    for i in range(1, 10):
        assert codec.compress(string, i) == [string[0:1], [0, len(string)-1]], f"test {i}"

    assert codec.compress("abcabcabc", 3) == ["abc", [0, 6]], f"test {i}"
    i += 1
    assert codec.compress("abababab", 2) == ["ab", [0, 6]], f"test {i}"
    i += 1
    assert codec.compress("abcdefabc", 3) == ["abcdef", [0, 3]], f"test {i}"
    i += 1
    assert codec.compress("abcdefabcdef", 3) == ["abcdef", [0, 6]], f"test {i}"
    i += 1
    assert codec.compress("abcabcabc", 2) == ["abc", [0, 6]], f"test {i}"
    i += 1
    assert codec.compress("xabcdabcdy", 2) == ["xabcda", [2, 3], "y"], f"test {i}"
    i += 1
    assert codec.compress("xabcdabcdy", 1) == ["xabcd", [1, 4], "y"], f"test {i}"
    i += 1
    assert codec.compress("xabcabcy", 2) == ["xabca", [2, 2], "y"], f"test {i}"
    i += 1


    assert codec.encode("abcdef", "defghiabc", 3) == [[3, 3], "ghi", [0, 3]], f"test {i}"
    i += 1
    assert codec.encode("abcdef", "defghiabc", 2) == ["d", [4, 2], "ghi", [0, 3]], f"test {i}"
    i += 1
    assert codec.encode("abcdef", "defghiabc", 1) == [[3, 3], "ghi", [0, 3]], f"test {i}"
    i += 1
    assert codec.encode("abc", "d", 3) == ["d"], f"test {i}"
    i += 1
    assert codec.encode("abc", "defghi", 3) == ["defghi"], f"test {i}"
    i += 1
    assert codec.encode("abcdef", "abcdef", 3) == [], f"test {i}"
    i += 1
    assert codec.encode("abc", "abcdef", 3) == [[0, 3], "def"], f"test {i}"
    i += 1
    assert codec.encode("aaaaa", "aaaaaaaaaa", 3) == [[0, 5], [0, 5]], f"test {i}"
    i += 1

    print(codec.encode("Est cupidatat aliquip dolore consequat proident.", "Ets cupidatat aliquip dolore coucou consequat proident.", 2))
    print(codec.encode("Lorem ipsum", "Lorm tipsum", 2))