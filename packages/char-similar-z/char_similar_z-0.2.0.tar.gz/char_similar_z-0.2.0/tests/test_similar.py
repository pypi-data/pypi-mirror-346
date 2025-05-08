import time

from char_similar_z import CharSimilarity


def test_similar():
    """
    测试汉字相似度计算
    """

    sim = CharSimilarity()
    char1 = "我"
    char2 = "他"
    for kind in ["shape", "pinyin"]:
        t0 = time.time()
        score = sim.std_cal_sim(char1, char2, kind=kind)
        t1 = time.time()
        print(f"相似度({char1}, {char2})[{kind}]: {score}, 用时: {round(t1 - t0, 4)}s")
