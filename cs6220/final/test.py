import feature_extraction as fe
import linear_regression as lr

TRAIN_FILE = "../dm_dataset/AP_train/AP_train.txt"
TEST_FILE = "../dm_dataset/AP_train/AP_test_par.txt"

if __name__ == '__main__':
	pubs,links = fe.load_data(TRAIN_FILE)
	D = fe.feature_extraction(pubs,links)
	n = D.shape[1]	
	w = lr.caculateW(D[:,:n-1],D[:,n-1])
	test_pubs,lin = fe.load_data(TEST_FILE)
	key_list = pubs.keys()
	print "Id,References"
	for p in test_pubs:
		test_D = fe.test_features(test_pubs[p],pubs)
		test_y = lr.predict(D[:,:n-1],w)
		top_idx = sorted(range(len(test_y)), key=lambda i: test_y[i], reverse=True)[:10]
		str_p = "%s," %p
		for i in top_idx:
			str_p += " %s" %key_list[i]
		print str_p
