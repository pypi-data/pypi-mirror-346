from sklearn.model_selection import train_test_split

def split_train_test(x, y, test_ratio=0.2):

    try:
        ratio = float(test_ratio)
        if not 0 < ratio < 1:
            print(f"⚠️ test_ratio={test_ratio} 不合法，使用默认值0.2")
            ratio = 0.2
    except:
        print(f"⚠️ test_ratio={test_ratio} 不是数字，使用默认值0.2")
        ratio = 0.2

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = ratio)
    return x_train, x_test, y_train, y_test
