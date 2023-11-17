# k8s-api-proxy

this is a simple proxy server that exposes k8s node info. 

##Instructions

Create a base64 encoded  api key and replace it in the deployment.yaml secret resource:

```
echo -n "secret1234" | base64
```

Apply the deplyment manifest:

```
kubectl apply deployment.yaml
```


curl new service:

```
curl -X GET http://<any-node-id>:30000/node-info -H "X-API-Key:secret1234"
```
