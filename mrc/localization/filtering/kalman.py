import math

import cv2
import numpy as np


class KalmanPredictor:
    def __init__(self):
        self.kf = cv2.KalmanFilter(4, 2)
        self.kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        self.kf.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
        self.kf.measurementNoiseCov = np.array([[100, 0], [0, 100]], np.float32)
        # self.kf.errorCovPre = np.array([[50, 0, 0, 0], [0, 50, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
        self.kf.processNoiseCov = np.array([[0.01, 0, 0, 0], [0, 0.01, 0, 0], [0, 0, 0.01, 0], [0, 0, 0, 0.01]],
                                           np.float32)
        # self.kf.errorCovPost = np.array([[1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)

    def update(self, r, phi):
        measurement = np.array([[np.float32(r)], [np.float32(phi)]])
        self.kf.correct(measurement)

    def predict(self):
        return self.kf.predict()


if __name__ == '__main__':
    kp = KalmanPredictor()
    measurements = [
        (48.22357865302437, -0.6563121057384881),
        (48.2088175334884, -0.6562690900788272),
        (48.171620306339854, -0.6562266264149114),
        (48.15728056964963, -0.6561536067071907),
        (48.164750041750224, -0.6560846347587544),
        (48.116448122718694, -0.6561609648321132),
        (48.13494979769769, -0.6561137453045656),
        (48.09039651718752, -0.6561645061644856),
        (48.10922785797993, -0.655941150698753),
        (48.07053699026814, -0.6560607935022115),
        (48.07561848517085, -0.6559268737744235),
        (48.109590896358455, -0.6559803958687201),
        (48.03530069033265, -0.6561556449154693),
        (48.07041043122841, -0.655809039605885),
        (48.0587194849574, -0.6555507649524854),  # Peak
        (48.052362329094876, -0.6554973752498995),
        (47.95650912921532, -0.6555359708143453),
        (47.88164933148326, -0.6552392867585791),
        (47.93356868823448, -0.6552354899896136),
        (47.873011757487475, -0.6551356424005775),
        (47.981645569449675, -0.6551786185302331),
        (47.80121618070892, -0.6547424926024118),
        (47.85604065643289, -0.6544696785998821),
        (47.713638621704476, -0.6540163806732693),
        (47.818773007957255, -0.6546238859091849),
        (47.88766230045588, -0.6548751352528289),
        (47.823754582005876, -0.6546395173881486),
        (47.66210572274977, -0.654561943154279),
        (47.764295148944164, -0.6553512452654314),
        (48.98016884660062, -0.6590300553958125),
        (53.064045970431216, -0.6563612387931296),
        (54.732326763629985, -0.6800046614077802),
        (55.351008828270864, -0.692421254697518),
        (56.42428480871924, -0.6984691480486629),
        (56.500971560990244, -0.6955224127990673),
        (56.68738971518934, -0.7007052333777891),
        (57.095534700834214, -0.723823088261599),
        (54.69664062139216, -0.7647429214822543),
        (52.37466117156677, -0.8117799984094444),
        (49.873044632855645, -0.8685276047831383),
        (48.95335204403513, -0.8823020097152895),
        (45.89133440627474, -0.9586804504957355),
        (44.195453990527746, -1.0091314866854832),
        (41.76616759024945, -1.077639029445803),
        (39.680732112814766, -1.1655689673555472),
        (37.2975706875395, -1.27855982863182),
        (130.1142816810917, -1.3368015605161916),
        (34.52125502464176, -1.4328281243820664),
        (33.15669356436219, -1.4889736085640968),
        (32.01668133108438, -1.5658650183716645),
        (31.089159171794137, -1.6361724052342477),
        (31.133027169833767, -1.6577067132207373),
        (30.182953219029677, -1.6972332844859668),
        (29.990040253429918, -1.7806966142844591),
        (30.07459763954752, -1.8450180279730632),
        (30.038701275338656, -1.9360462920566597),
        (30.276469076226242, -1.992652981205745),
        (29.432470811067443, -2.00502799579947),
        (28.827928923254376, -2.0280897437673744),
        (28.150336566386667, -2.0483868618180607),
        (27.587177522941673, -2.051788468615922),
        (27.140363987534997, -2.059661864319927),
        (26.436861552351598, -2.064657859939825),
        (25.4426463635281, -2.041091003364791),
        (24.941650900214714, -1.9929469257429098),
        (24.68459658705208, -1.946348028547416),
        (24.40469474045046, -1.8716292669582848),
        (24.519755576527096, -1.7964409199152553),
        (24.861504781159162, -1.703368375045629),
        (26.177080596296985, -1.6206435085465432),
        (27.37692344321758, -1.521353639155238),
        (28.54845200179053, -1.440953939846758),
        (31.167835065681743, -1.3357926155613982),
        (33.848837731997314, -1.247230675766164),
        (37.31074688248437, -1.1313571498430013),
        (39.90995806567982, -1.055532876130014),
        (44.15579927913379, -0.9786094949932648),
        (46.42236845273441, -0.9431816433167993),
        (49.001754796534854, -0.9022690587829282),
        (52.72919491164011, -0.8345273413212728),
        (53.217793456958844, -0.7789170181572955),
        (52.90138488158783, -0.7351609887550025),
        (50.133014475138104, -0.6962973220737815),
        (46.59203906892108, -0.6434367359250593),
        (40.28838718162468, -0.6181412370371132),
        (35.40096282304214, -0.5832164531110172),
        (31.49282828015183, -0.4742981405424702),
        (28.92956859288819, -0.3987230293392607),
        (28.612163829617472, -0.3686656195350756),
        (28.56159779060822, -0.3672396994568369),
        (28.568252929740414, -0.36750605475211634)]
    rs, phis = [], []
    rspred, phispred = [], []
    xs = range(len(measurements))
    for i, m in enumerate(measurements):
        r, phi = m
        rs.append(r)
        phis.append(phi)

        kp.update(r, phi)
        _r, _phi, v, a = kp.predict()
        rspred.append(_r)
        phispred.append(_phi)

    import matplotlib.pyplot as plt

    plt.plot(xs, rs, xs, rspred)
    plt.show()
    # plt.plot(xs, phis, xs, phispred)
    # plt.show()
