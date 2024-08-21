<!DOCTYPE html>
<html lang="en">
<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Company Type</title>

    <!-- Custom fonts for this template -->
    <link href="{% static 'assests/vendor/fontawesome-free/css/all.min.css' %}" rel="stylesheet" type="text/css">
    <link
        href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i"
        rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="{% static 'assests/css/sb-admin-2.min.css' %}" rel="stylesheet">

    <!-- Custom styles for this page -->
    <link href="{% static 'assests/vendor/datatables/dataTables.bootstrap4.min.css' %}" rel="stylesheet">

</head>

<body id="page-top">

    <!-- Page Wrapper -->
    <div id="wrapper">

        <!-- Sidebar -->
        <?php include 'navbar.php' ?>
        <!-- End of Sidebar -->

        <!-- Content Wrapper -->
        <div id="content-wrapper" class="d-flex flex-column">

            <!-- Main Content -->
            <div id="content">

                <!-- Topbar -->
                <?php include 'topbar.php' ?>
                <!-- End of Topbar -->

                <!-- Begin Page Content -->
                <div class="container-fluid">

                    <!-- Page Heading -->
                    <h1 class="h3 mb-2 text-gray-800">Information of Company Type</h1>

                    <!-- Add-Doctor Form -->
                    <div class="card o-hidden border-0 shadow-lg my-5">
                        <div class="card-body p-0">
                            <!-- Nested Row within Card Body -->
                            <div class="row">
                                <!-- <div class="col-lg-5 d-none d-lg-block bg-register-image"></div> -->
                                <div class="col-lg-12">
                                    <div class="p-5">
                                        <div class="text-center">
                                            <h1 class="h4 text-gray-900 mb-4"></h1>
                                        </div>
                                            <form method="post" enctype="multipart/form-data">
                                                <div class="form-group">
                                                    <div class="col-sm-12 mb-3 mt-3 mb-sm-0">
                                                        <input type="text" class="form-control form-control-user" name="companyType"
                                                            placeholder="Company Type" required>
                                                    </div>
                                                    <button type="submit" class="btn btn-primary btn-user btn-block" name="submit">
                                                        Submit
                                                    </button>
                                                </div>
                                            </form>
                                        <hr>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- DataTales Example -->
                    <div class="card shadow mb-4">
                        <div class="card-header py-3">
                            <h6 class="m-0 font-weight-bold text-primary">Table</h6>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
                                    <thead>
                                        <tr>
                                            <th>NO.</th>
                                            <th>Company Type</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tfoot>
                                        <tr>
                                            <th>NO.</th>
                                            <th>Company Type</th>
                                            <th>Action</th>
                                        </tr>
                                    </tfoot>
                                    <tbody>
                                    <?php 
                                    $number = 1;
                                    for()
                                    { ?>
                                        <tr>
                                            <td><?php echo $number ?></td>
                                            <td><?php echo $Ctype_name ?></td>
                                            <td>
                                                <a href="" class="btn btn-primary mt-2">Update</a>
                                                <a href="" class="btn btn-danger mt-2">Delete</a>
                                            </td>                                            
                                        </tr>
                                    <?php
                                    $number++ 
                                        } 
                                    ?>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                </div>
                <!-- /.container-fluid -->

            </div>
            <!-- End of Main Content -->

            <!-- Footer -->
            <?php include 'footer.php' ?>
            <!-- End of Footer -->

        </div>
        <!-- End of Content Wrapper -->

    </div>
    <!-- End of Page Wrapper -->

    <!-- Scroll to Top Button-->
    <a class="scroll-to-top rounded" href="#page-top">
        <i class="fas fa-angle-up"></i>
    </a>

    <!-- Logout Modal-->
    <?php include 'logout.php' ?>

    <!-- Bootstrap core JavaScript-->
    <script src="{% static 'assests/vendor/jquery/jquery.min.js' %}"></script>
    <script src="{% static 'assests/vendor/bootstrap/js/bootstrap.bundle.min.js' %}"></script>

    <!-- Core plugin JavaScript-->
    <script src="{% static 'assests/vendor/jquery-easing/jquery.easing.min.js' %}"></script>

    <!-- Custom scripts for all pages-->
    <script src="{% static 'assests/js/sb-admin-2.min.js' %}"></script>

    <!-- Page level plugins -->
    <script src="{% static 'assests/vendor/datatables/jquery.dataTables.min.js' %}"></script>
    <script src="{% static 'assests/vendor/datatables/dataTables.bootstrap4.min.js' %}"></script>

    <!-- Page level custom scripts -->
    <script src="{% static 'assests/js/demo/datatables-demo.js' %}"></script>

</body>
</html>