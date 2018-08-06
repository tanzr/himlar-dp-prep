<%inherit file="main.mak"/>
<div class="row uninett-color-white uninett-whole-row uninett-padded">
  <h2>${user.name}</h2>
% if was_provisioned:
  <p>UH-IaaS was already prepared for Dataporten</p>
% else:
  <p>UH-IaaS prepared for Dataporten</p>
% endif
% if api_pw:
  <h3>API access</h3>
  <p>Username: '${api_user_name}'
  <br/>
  Password: '${api_pw}'</p>
  <p>NB! Remember to write the password down for later use.</p>
% endif
  <a href="${dashboard_url}" class="btn btn-default uninett-login-btn">
    <span class="glyphicon glyphicon-user uninett-fontColor-red"></span>
    Continue to UH-IaaS
  </a>
  <br/>
% if was_provisioned:
  <a style="color:#eb212e" href="/reset" class="btn btn-underline">Reset API password</a>
% endif
  <br/>
  <p>You may be sent back to Dataporten again.</p>
</div>
