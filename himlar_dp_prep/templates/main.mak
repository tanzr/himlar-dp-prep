<!DOCTYPE html>
<html lang="${request.locale_name}">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="shortcut icon" href="${request.static_url('himlar_dp_prep:uninett-theme/ico/favicon.ico')}">

    <title>UH IaaS via Dataporten</title>

    <!-- Bootstrap core CSS -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this scaffold -->
    <link href="${request.static_url('himlar_dp_prep:uninett-theme/css/uninett.css')}" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="//oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="//oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
  </head>

<body>

    <!-- Fixed navbar -->
    <div class="navbar navbar-default navbar-fixed-top" role="navigation">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse"> <span class="sr-only">Toggle navigation</span> <span class="icon-bar"></span> <span class="icon-bar"></span> <span class="icon-bar"></span> </button>
                <a class="navbar-brand" href="/"><img src="${request.static_url('himlar_dp_prep:uninett-theme/images/UNINETT_logo.svg')}" alt="Uninett logo" type="image/svg+xml"></a>
            </div>
            <div class="navbar-department">
                <div class="department">Dataporten</div>
            </div>
            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                </ul>
            </div>
        </div>
    </div>

    <div class="container">

        ${self.body()}

        <hr class="uninett-hr-divider">
        <div class="row">
            <div class="col-lg-12">
                <div class="footer-uninett">
                    <div class="footer-content-uninett">
                            <div class="footer-logo"> <img src="${request.static_url('himlar_dp_prep:uninett-theme/images/Uninett_pil_rod.svg')}" alt="Uninett logo" type="image/svg+xml"></div>
                            <div class="footer-uninett-department">UNINETT AS 2017</div>
                    </div>
                    <div class="clearfix"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- /container -->

    <!-- Bootstrap core JavaScript -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://code.jquery.com/jquery-1.11.3.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>

</body>
</html>
