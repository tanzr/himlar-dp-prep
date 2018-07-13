<%inherit file="main.mak"/>
<div class="row uninett-color-white uninett-whole-row uninett-padded">
  <h2>${header}</h2>
  <p>${message}</p>
% if provisioned:
 <p>Continue to UH-IaaS <a href="${dashboard_url}">[her].</a></p>
 <p>You may be sent back to Dataporten again.</p>
%else:
  <p>Sorry, you have not signed up to UH-IaaS yet!</p>
% endif
</div>
