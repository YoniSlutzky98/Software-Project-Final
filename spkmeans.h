double** weighted_adj_mat(double** obs, int n, int d);
double** diag_deg_mat(double** wam, int n);
double** norm_graph_lap(double** wam, double** ddg, int n);
double** jacobi_eval_evec(double** mat, int n);
double euclid_dist(double* x, double* y, int columns);
void free_matrix(double** mat, int n);