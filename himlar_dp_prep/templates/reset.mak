<%inherit file="main.mak"/>
<div class="row uninett-color-white uninett-whole-row uninett-padded">
  <h2>UH-IaaS via Dataporten</h2>
  <br/>
% if was_provisioned:
  <h3>Reset API password</h3>
  <p>Username: '${api_user_name}'
  <br/>
  Password: '${api_pw}'</p>
  <p>NB! Remember to write the password down for later use.</p>
  <a href="https://dashboard.vagrant.iaas.intern/dashboard/auth/login/" class="btn btn-default uninett-login-btn">
    <span class="glyphicon glyphicon-user uninett-fontColor-red"></span>
    Continue to UH-IaaS
  </a>
%else:
  <p>You have not signed up to UH-IaaS yet!</p>
  <a href="/login" class="btn btn-default uninett-login-btn">
    <span class="glyphicon glyphicon-user uninett-fontColor-red"></span>
    Sign up
  </a>
% endif
  <br/>
  <p>You may be sent back to Dataporten again.</p>
</div>
