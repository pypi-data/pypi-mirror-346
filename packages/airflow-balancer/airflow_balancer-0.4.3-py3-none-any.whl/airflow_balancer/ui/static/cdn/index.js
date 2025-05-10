document.addEventListener("DOMContentLoaded",async()=>{let u=window.__AIRFLOW_BALANCER_CONFIG__,e=document.getElementById("airflow-balancer-root");u===void 0&&(e.innerHTML=`
        <div class="alert alert-danger" role="alert">
            <strong>Airflow Balancer Config not found!</strong>
            <p>Please make sure you are running the Airflow Balancer with the correct configuration.</p>
        </div>
        `);let t=JSON.parse(u);e.innerHTML=`
    <div class="airflow-balancer-defaults">
        <h2>Defaults</h2>
        <div class="form-group">
            <label for="default-username">Default Username</label>
            <input type="text" class="form-control" id="default-username" disabled value="${t.default_username||""}">
            <small class="form-text text-muted">Default username for all hosts.</small>
            <br>
            <label for="default-password-variable">Default Password Variable</label>
            <input type="text" class="form-control" id="default-password-variable" disabled value="${t.default_password_variable||""}">
            <small class="form-text text-muted">Default password variable for all hosts.</small>
            <br>
            <label for="default-password-variable-key">Default Password Variable Key</label>
            <input type="text" class="form-control" id="default-password-variable-key" disabled value="${t.default_password_variable_key||""}">
            <small class="form-text text-muted">Default password variable key for all hosts.</small>
            <br>
            <label for="default-key-file">Default Key File</label>
            <input type="text" class="form-control" id="default-key-file" disabled value="${t.default_key_file||""}">
            <small class="form-text text-muted">Default key file for all hosts.</small>
            <br>
            <label for="default-size">Default Size</label>
            <input type="number" class="form-control" id="default-size" disabled value="${t.default_size||0}">
            <small class="form-text text-muted">Default size for all hosts.</small>
        </div>
    </div>`;let p=`
    <div class="airflow-balancer-hosts">
      <h2>Hosts</h2>
      <table class="table table-striped table-bordered table-hover">
        <thead>
          <tr>
            <th>Name</th>
            <th>Username</th>
            <th>Password</th>
            <th>Password Variable</th>
            <th>Password Variable Key</th>
            <th>Key File</th>
            <th>OS</th>
            <th>Pool</th>
            <th>Size</th>
            <th>Queues</th>
            <th>Tags</th>
          </tr>
        </thead>
        <tbody>`;t.hosts?.forEach(a=>{let l=a.name,r=a.username,o=a.password||"None",n=a.password_variable||"None",d=a.password_variable_key||"None",f=a.key_file||"None",b=a.os||"None",c=a.pool||"None",h=a.size||0,m=a.queues.map(i=>`<span class="badge badge-secondary">${i}</span>`).join(" "),_=a.tags.map(i=>`<span class="badge badge-secondary">${i}</span>`).join(" ");p+=`
          <tr>
            <td><span>${l}</span></td>
            <td><span>${r}</span></td>
            <td><span>${o}</span></td>
            <td><span>${n}</span></td>
            <td><span>${d}</span></td>
            <td><span>${f}</span></td>
            <td><span>${b}</span></td>
            <td><span>${c}</span></td>
            <td><span>${h}</span></td>
            <td>${m}</td>
            <td>${_}</td>
          </tr>
        `}),e.innerHTML+=p;let s=`
    <div class="airflow-balancer-ports">
      <h2>Ports</h2>
      <table class="table table-striped table-bordered table-hover">
        <thead>
          <tr>
            <th>Name</th>
            <th>Host</th>
            <th>Port</th>
            <th>Tags</th>
          </tr>
        </thead>
        <tbody>`;t.ports?.forEach(a=>{let l=a.name,r=a.tags.map(d=>`<span class="badge badge-secondary">${d}</span>`).join(" "),o=a.host_name||a.host.name,n=a.port;s+=`
          <tr>
            <td><span>${l}</span></td>
            <td><span>${o}</span></td>
            <td><span>${n}</span></td>
            <td>${r}</td>
          </tr>
        `}),s+=`
        </tbody>
        </table>
    </div>
    `,e.innerHTML+=s});
//# sourceMappingURL=index.js.map
