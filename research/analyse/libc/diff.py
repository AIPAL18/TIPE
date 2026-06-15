# import time
# from difflib import SequenceMatcher

# with open("libc.so.5", "rb") as f:
#     libc5 = f.read()
#     f.close()

# with open("libc.so.6", "rb") as f:
#     libc6 = f.read()
#     f.close()

# def similarity_percentage():
#     return SequenceMatcher(None, libc5, libc6).ratio() * 100


# if __name__ == "__main__":
#     start_temp = time.time()
#     valeur = similarity_percentage
#     end = time.time()
#     print(f"{valeur = }")
#     t = (end - start_temp) / 60
#     print(f"{t = } minutes")


# # 14.67173679214199 ~ 14.7
