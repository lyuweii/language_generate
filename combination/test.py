import pytest
import sound as sd

def test_yunmu():
    yunmu = sd.YunMu.random_yunmu()
    print(yunmu)

def test_shengmu():
    shengmu = sd.ShengMu.random_shengmu()
    print(shengmu)



if __name__ == "__main__":
    #pytest.main([__file__])
    test_yunmu()
    test_shengmu()