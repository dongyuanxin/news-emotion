if __name__=='__main__':
    ###### 生成样本 #####
    best_vector = 'outofdict'
    best_model = 4 # 代表Logistic回归
    less_index = (resultY[best_vector]==0)
    less_vector = resultX[best_vector][less_index,:] # 所有中性样本

    new_size = int(0.25*len(less_vector))
    new_vector = np.empty((new_size,len(less_vector[0]))) # 新生成的训练集
    new_tag = np.ones(new_size)
    # print(new_vector.shape)
    for index in range(new_size):
        my_generator = GenerateSample(less_vector,topk=5)
        new_vector[index] = my_generator.generate()

    new_x_list = resultX[best_vector].tolist()
    new_x_list.extend(new_vector.tolist())
    new_x = np.array(new_x_list) # 最新生成的训练向量

    new_y_list = resultY[best_vector].tolist()
    new_y_list.extend(new_tag.tolist())
    new_y = np.array(new_y_list)
    print(len(new_x))
    print(len(new_y))
    rate = loocv(new_x,new_y,mode = best_model)
    print(rate)