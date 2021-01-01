import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

flux_mean = [0.03414045288547348, 0.11285154585293306, 0.25579615259211447, 0.46386801189831084, 0.6506196670114369,
             0.8082168436541028, 0.9270710209653598, 0.9781612188646129, 0.9858558315213521, 0.9630488544131711,
             0.8685615885278193, 0.7133254176219329, 0.5274477224531979, 0.2852134350996563, 0.12484371099090205,
             0.03828647491787618]

flux_std = [0.007637359872649376, 0.017492888212822067, 0.03099312924230917, 0.047591648378269125, 0.047250592403443786,
            0.046430176430566676, 0.04347162978502152, 0.021968260813257357, 0.01775671784153132, 0.03465659875449356,
            0.03182338998304291, 0.029524607976838063, 0.026725426407510237, 0.026161961823681943, 0.01536767084323428,
            0.006059329921564905]

ka_lst = [1.0456, 1.0494, 1.0778, 1.0498, 1.0338, 1.0476, 1.0656, 1.0522, 1.0424, 1.0694, 1.06, 1.0564, 1.0668, 1.0628,
          1.04, 1.0478, 1.0628, 1.0606, 1.0744, 1.05, 1.0572, 1.0604, 1.0658, 1.059, 1.0464, 1.0502, 1.0668, 1.031,
          1.0644, 1.0408]

kt_lst = [1.0567692564786049, 1.0391009511260823, 1.072241701876324, 1.0648677671435103, 1.0472826652831333,
          1.0512928238973112, 1.0467221065173937, 1.0596690386811505, 1.0534998543766882, 1.063308159677939,
          1.062878206524919, 1.0682362282224087, 1.0504621961673772, 1.0444134574926265, 1.0520391014178458,
          1.0527606063359771, 1.0529996920080087, 1.0679619382462202, 1.0508123433895686, 1.0526555128760815,
          1.059939321491057, 1.0725898789213686, 1.0451951666852644, 1.0532420114267111, 1.0643245930400538,
          1.0578115357859508, 1.0732556590945785, 1.0579903975461582, 1.060817443241933, 1.0704003690673765]

x = range(-75, 80, 10)
plt.plot(x, flux_mean)
plt.plot(x, flux_std)
plt.show()
plt.plot(ka_lst)
plt.plot(kt_lst)
plt.show()

'''
the final keff-absorb is 1.05524, the std is 0.011628905721342057 
the final keff-track is 1.0575179994679875, the std is 0.009125772631219437 
'''

'''
江世航的计算通量
'''
f_sh = [92789.23447457408, 246712.66496995164, 434610.30777825706, 683463.7286810682, 1033486.6405338893,
        1523566.2313395967, 2065275.471464209, 2602325.19968838, 3037262.265650585, 3418110.698444863,
        3758213.7255707076, 4036969.4768342, 4284479.945302467, 4467250.014069865, 4566340.516480997, 4606002.52834031,
        4576518.037335033, 4502138.689268878, 4379404.296505364, 4193006.381664279, 3947646.494760516, 3631113.44111467,
        3294145.9267592514, 2897589.674936582, 2473556.6647837656, 2013323.3830282113, 1436516.3365520074,
        1004226.4664410751, 669321.7508254339, 424063.75461964734, 242867.57072550364, 91018.68661937155]

f_sh = [(f_sh[2*i] + f_sh[2*i + 1]) for i in range(int(len(f_sh) / 2))]
f_m = max(f_sh)
f_sh = [f_sh[i] / f_m for i in range(len(f_sh))]
flux_mean = [(flux_mean[i]+flux_mean[15-i])/2 for i in range(len(flux_mean))]
f_sh = [(f_sh[i]+f_sh[15-i])/2 for i in range(len(f_sh))]

plt.plot(f_sh, label='jiang')
plt.plot(flux_mean, label='shen')
plt.legend()
plt.show()

rela = [abs(flux_mean[i]-f_sh[i])/flux_mean[i]*100 for i in range(len(flux_mean))]
print(rela)