<%inherit file="main.mak"/>
<div class="row uninett-color-white uninett-whole-row uninett-padded">
  <h2>${user.name}</h2>
% if was_provisioned:
  <p>UH-IaaS var allerede klargjort for Dataporten</p>
% else:
  <p>UH-IaaS klargjort for Dataporten</p>
% endif
% if local_pw:
  <h3>API-tilgang</h3>
  <p>Brukernavn er '${local_user_name}' og passord er '${local_pw}'.
  <br/>
  NB! Husk å skrive dette ned til senere bruk.</p>
% endif
  <a href="${dashboard_url}" class="btn btn-default uninett-login-btn">
    <span class="glyphicon glyphicon-user uninett-fontColor-red"></span>
    Fortsett til UH-IaaS
  </a>
  <p>Du blir muligens sendt innom Dataporten igjen først.</p>
</div>
