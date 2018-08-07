<%inherit file="main.mak"/>
<div class="row uninett-color-white uninett-whole-row uninett-padded">
  <h2>${header}</h2>
  <p>${message}</p>
% if provisioned:
 <p>Continue to UH-IaaS <a href="${dashboard_url}">[her].</a></p>
%else:
  <p>You have not signed up to UH-IaaS yet.</p>
  <p>Before signing up to UH-IaaS, make sure that you have read and understood our
  <a href="http://docs.uh-iaas.no/en/latest/terms-of-service.html" target="blank">
  Terms of Service</a>.</p>
% endif
 <p>You may be sent back to Dataporten again.</p>
</div>
