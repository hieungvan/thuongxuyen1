import matplotlib.pyplot as plt
def ve_bieu_do_cot(categories, values):
  
    plt.bar(categories, values)

    plt.title('Số lượng các loại điểm A, B, C, D, E, F')
    plt.xlabel('Loại điểm')
    plt.ylabel('Số lượng')

    
    plt.show()
categories = ['A', 'B', 'C', 'D', 'E', 'F']
values = [10, 20, 15, 5, 8, 2]

ve_bieu_do_cot(categories, values)
