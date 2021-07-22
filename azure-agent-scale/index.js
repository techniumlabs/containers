import * as azdev from "azure-devops-node-api";
//  import { BuildStatus } from "azure-devops-node-api/interfaces/BuildInterfaces";
import * as k8s from '@kubernetes/client-node'



let orgUrl = process.env.URL 
let token = process.env.TOKEN

let authHandler = azdev.getPersonalAccessTokenHandler(token);

let connection = new azdev.WebApi(orgUrl, authHandler);
const kc = new k8s.KubeConfig();
kc.loadFromDefault();
const k8sApi = kc.makeApiClient(k8s.AppsV1Api);

(async () => {
    let buildAPI = await connection.getBuildApi()
    try {
        let project_name = 'devops'
        let nameSpace = 'default'
        let queue_running_status = 33
        let builds = await buildAPI.getBuilds(project_name, undefined, undefined, undefined, undefined, undefined, undefined, undefined, queue_running_status)
        // console.log(JSON.stringify(builds))
        let pool_details = {}

        builds.forEach(build => { // scale up
            let pool_name = build.queue?.pool?.name
            if (pool_name in pool_details) {
                pool_details[pool_name] += 1
            } else {
                pool_details[pool_name] = 1
            }
        })
        let deployments = await k8sApi.listNamespacedDeployment(nameSpace)
        let deployment_names = []
        deployments.body?.items.forEach(deployment => {
            if (deployment.spec.replicas) {
                deployment_names.push(deployment.metadata.name)
            }

        })
        deployment_names.forEach(name => {
            if (!(name in pool_details)) { //scale down
                pool_details[name] = 0
            }
        })

        console.log(pool_details, deployment_names)
        for (let key in pool_details) {
            try {
               await scaleDeployment(key, nameSpace, pool_details[key])
            } catch (error) {
                console.log(error)
            }

        }

    } catch (e) {
        console.log(e)
    }
})()


 function scaleDeployment(name, nameSpace, replicas) {
   return new Promise(async(resove, reject) => {
        try {
            let data = await k8sApi.readNamespacedDeployment(name, nameSpace)
            let deployment = data.body
            if (deployment.spec.replicas < replicas || replicas == 0) {
                deployment.spec.replicas = replicas
                await k8sApi.replaceNamespacedDeployment(name, nameSpace, deployment)
            }
            resove({status:"success"})
        } catch (error) {
            reject(error)
        }
    })


}