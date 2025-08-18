
## CD Plan
Our Continuous Deployment (CD) strategy uses GitHub Actions to deploy our containerized application to Amazon Web Services (AWS). The process follows these steps:

Trigger: A successful merge to the main branch kicks off the CI/CD pipeline.

CI Checks: The pipeline first runs all linting and testing jobs to ensure code quality.

Build & Push: A new, version-tagged Docker image is built for the API and pushed to the Amazon Elastic Container Registry (ECR).

Deploy: The final step in the pipeline uses the AWS CLI to update the task definition for our application on Amazon Elastic Container Service (ECS) with the new image tag.

Release: ECS automatically performs a rolling deployment, gracefully starting the new containers and stopping the old ones, ensuring a zero-downtime release for our users.