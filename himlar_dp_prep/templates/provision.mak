<%inherit file="main.mak"/>
<div class="row uninett-color-white uninett-whole-row uninett-padded">
  <h2>${header}</h2>
  <p>${message}</p>
% if provisioned:
 <p>Fortsett til UH-IaaS <a href="${dashboard_url}">[her].</a></p>
 <p>Du blir muligens sendt innom Dataporten igjen først.</p>
% endif
</div>
