if __name__=='__main__':
    ##### 二分类 #####
    best_vector = 'outofdict'
    best_model = 4  #
    new_index = (resultY[best_vector] != 0)
    print(new_index)
    print(len(new_index))
    new_x = resultX[best_vector][new_index,:]  # 所有中性样本
    new_y = resultY[best_vector][new_index]
    rate = loocv(new_x, new_y, mode=best_model)
    print(rate)