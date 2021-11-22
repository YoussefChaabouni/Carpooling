import numpy as np

def algorithm_4(drivers,rider):

	org_r = rider.org
	wd = 0
	wt = 0
	t_prime = t_PLUS(rider,org_r)

	# --------------- FIRST MILE --------------- #
	t_first = np.Infinity


	for d in drivers:

		m_dst_d = d.m_dst
		d_trajectory = d.trajectory
		m_dst_r = rider.m_dst
		s_org_r = rider.s_org

		if m_dst_d == m_dst_r and s_org_r in d_trajectory :

			t_chap,w_chap_t,w_chap_d = Algo2() # APPLIQUER L'ALGORITHME 2

			if wd + w_chap_d <= 2500  and  wt + w_chap_t <= 45*60  and  t_chap < t_first: # les longueurs en Mètres et le temps en Secondes

				t_first = t_chap
				wd 		= wd + w_chap_d
				wt 		= wt + w_chap_t



	if t_first > np.Infinity:
		# si ce n'est pas possible d'amener le rider directement à la station, alors cherchons le meeting-point m_prime le plus proche de la station s_org_r qui sera desservit par une voiture 

		for d in drivers:

			m_dst_d = d.m_dst_d
			rider.s_org_r = s_org_r

			if m_dst_d == m_prime:

				t_chap,w_chap_t,w_chap_d = Algo2() # APPLIQUER L'ALGORITHME 2

				if w_chap_d <= 2500  and  w_chap_t <= 45*60  and  t_chap < t_first: # les longueurs en Mètres et le temps en Secondes

					t_first = t_chap
					wd 		= w_chap_d
					wt 		= w_chap_t



	if t_first > np.Infinity:
		# le seul choix du rider est donc de marcher jusqu'à la station la plus proche

		w_chap_d = distance(org_r,s_org_r)

		if w_chap_d < 2500 :

			t_first = t_prime + walk(org_r,s_org_r)
			wd 		= w_chap_d



	if t_first > np.Infinity:
		# le rider ne peut pas atteindre la station s_org_r

		t_prime = np.Infinity

	# --------------- TRAIN --------------- #
	t_prime += 1*60 # admettons qu'une minute est necessaire afin de monter dans le train une fois qu'on a atteint la station


	# --------------- LAST MILE --------------- #

	t_last = np.Infinity

	for d in drivers:

		m_dst_d = d.m_dst
		d_trajectory = d.trajectory
		m_dst_r = rider.m_dst
		s_dst_r = rider.s_dst

		if m_dst_d == m_dst_r and s_dst_r in d_trajectory :

			t_chap,w_chap_t,w_chap_d = Algo2() # APPLIQUER L'ALGORITHME 2

			if wd + w_chap_d <= 2500  and  wt + w_chap_t <= 45*60  and  t_chap < t_last: # les longueurs en Mètres et le temps en Secondes

				t_last = t_chap
				wd 		= wd + w_chap_d
				wt 		= wt + w_chap_t



	if t_last > np.Infinity:
		# si ce n'est pas possible d'amener le rider directement à la station, alors cherchons le meeting-point m_prime le plus proche de la station s_dst_r qui sera desservit par une voiture 

		for d in drivers:

			m_dst_d = d.m_dst_d
			rider.s_dst_r = s_dst_r

			if m_dst_d == m_prime:

				t_chap,w_chap_t,w_chap_d = Algo2() # APPLIQUER L'ALGORITHME 2

				if w_chap_d <= 2500  and  w_chap_t <= 45*60  and  t_chap < t_last: # les longueurs en Mètres et le temps en Secondes

					t_last = t_chap
					wd 		= w_chap_d
					wt 		= w_chap_t



	if t_last > np.Infinity:
		# le seul choix du rider est donc de marcher jusqu'à la station la plus proche

		w_chap_d = distance(dst_r,s_dst_r)

		if w_chap_d < 2500 :

			t_last = t_prime + walk(dst_r,s_dst_r)
			wd 		= w_chap_d



	if t_last > np.Infinity:
		# le rider ne peut pas atteindre la station s_dst_r

		t_prime = np.Infinity	


	return 0