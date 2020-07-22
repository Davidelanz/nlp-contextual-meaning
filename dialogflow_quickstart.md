
# Quickstart: Setup

<div class="devsite-article-body clearfix"><style>:root{--df-gcp-diagram-blue: #e1f6fe;--df-gcp-diagram-blue-dark: #04579b;--df-gcp-diagram-green: #e2f3ec;--df-gcp-diagram-yellow: #fef7e0;--df-gcp-diagram-lilac: #ede7f7;--df-gcp-diagram-lilac-grey: #e8eaf6;--df-gcp-diagram-grey: #eaedef;--df-gcp-header-grey: #e8eaed;--df-gcp-text-bg-light-grey: #f5f5f5;--df-gcp-text: #202124}pre{tab-size:2}</style>

This guide provides all required setup steps to start using Dialogflow.

## Before you begin

You should do the following before reading this guide:

1.  Read [Dialogflow basics](https://cloud.google.com/dialogflow/docs/basics).
2.  Read [Editions](https://cloud.google.com/dialogflow/docs/editions).

## About the Google Cloud Console

The Google Cloud Console ([visit documentation](https://support.google.com/cloud/answer/3465889?hl=en&ref_topic=3340599), [open console](https://console.cloud.google.com/)) is a web UI used to provision, configure, manage, and monitor systems that use Google Cloud products. You use the Google Cloud Console to set up and manage Dialogflow resources.

## Create a project

To use services provided by Google Cloud, you must create a _project_. A project organizes all your Google Cloud resources. A project consists of a set of collaborators, enabled APIs (and other resources), monitoring tools, billing information, and authentication and access controls. You can create one project, or you can create multiple projects and use them to organize your Google Cloud resources in a [resource hierarchy](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy). When creating a project, take note of the [project ID](https://cloud.google.com/resource-manager/docs/creating-managing-projects#identifying_projects). You will need this ID to make API calls. For more information on projects, see the [Resource Manager documentation](https://cloud.google.com/resource-manager/docs/creating-managing-projects).

The Dialogflow Console ([visit documentation](https://cloud.google.com/dialogflow/docs/console), [open console](https://dialogflow.cloud.google.com/)) can optionally create a basic project for you when you create an agent. If you plan on using your project for more than just basic access to a [free edition](https://cloud.google.com/dialogflow/docs/editions), or you plan on using the API, you should create a project with the Google Cloud Console as described below.

We recommend that you create separate projects for experiments, testing, and production. Each project can only create one [Dialogflow Agent](https://cloud.google.com/dialogflow/docs/agents-overview). If you need multiple agents, you will need to create multiple projects.

In the Cloud Console, on the project selector page, select or create a Cloud project.

[Go to the project selector page](https://console.cloud.google.com/projectselector2/home/dashboard)

## Enable billing

>**Note:** <span>You can skip this step if you are only using a free [Dialogflow edition](https://cloud.google.com/dialogflow/docs/editions).</span></aside>

A billing account is used to define who pays for a given set of resources, and it can be linked to one or more projects. Project usage is charged to the linked billing account. In most cases, you configure billing when you create a project. For more information, see the [Billing documentation](https://cloud.google.com/billing/docs).

Make sure that billing is enabled for your Google Cloud project. [Learn how to confirm billing is enabled for your project](https://cloud.google.com/billing/docs/how-to/modify-project).

## Enable the API

>**Note:** <span>You can skip this step if you are using the Dialogflow Console to create your project.</span></aside>

You must enable the Dialogflow API for your project. For more information on enabling APIs, see the [Service Usage documentation](https://cloud.google.com/service-usage/docs/enable-disable).

Enable the Dialogflow API.

[Enable the API](https://console.cloud.google.com/flows/enableapi?apiid=dialogflow.googleapis.com)

## Set up authentication

>**Note:** <span>You can skip this step if you will not be using the API.</span></aside>

If you plan to use the Dialogflow API, you need to set up authentication. Any client application that uses the API must be authenticated and granted access to the requested resources. This section describes important authentication concepts and provides steps for setting it up. For more information, see the [Google Cloud authentication overview](https://cloud.google.com/docs/authentication).

### About service accounts

There are multiple options for authentication, but it is recommended that you use _service accounts_ for authentication and access control. A service account provides credentials for applications, as opposed to end-users. Service accounts are owned by projects, and you can create many service accounts for a project. For more information, see [Understanding service accounts](https://cloud.google.com/iam/docs/understanding-service-accounts).

### About roles

When an identity calls an API, Google Cloud requires that the identity has the appropriate permissions. You can grant permissions by granting _roles_ to a service account. For more information, see the [Identity and Access Management (IAM) documentation](https://cloud.google.com/iam/docs/understanding-roles).

For the purpose of trying the Dialogflow API, you can use the **Project > Owner** role in steps below, which grants the service account full access to the project. For more information on roles specific to Dialogflow, see the [Dialogflow access control document](https://cloud.google.com/dialogflow/docs/access-control).

### About service account keys

Service accounts are associated with one or more public/private key pairs. When you create a new key pair, you download the private key. Your private key is used to generate credentials when calling the API. You are responsible for security of the private key and other management operations, such as key rotation.

### Create a service account and download the private key file

Set up authentication:

1.  In the Cloud Console, go to the **Create service account key** page.

    [Go to the Create Service Account Key page](https://console.cloud.google.com/apis/credentials/serviceaccountkey)
2.  From the **Service account** list, select **New service account**.
3.  In the **Service account name** field, enter a name.
4.  From the **Role** list, select **Project** > **Owner**.

    <div class="note">**Note**: The **Role** field authorizes your service account to access resources. You can view and change this field later by using the [Cloud Console](https://console.cloud.google.com/). If you are developing a production app, specify more granular permissions than **Project > Owner**. For more information, see [granting roles to service accounts](https://cloud.google.com/iam/docs/granting-roles-to-service-accounts).</div>

5.  Click **Create**. A JSON file that contains your key downloads to your computer.

### Use the service account key file in your environment

Provide authentication credentials to your application code by setting the environment variable `GOOGLE_APPLICATION_CREDENTIALS`. Replace <var translate="no">[PATH]</var> with the file path of the JSON file that contains your service account key. This variable only applies to your current shell session, so if you open a new session, set the variable again.

<devsite-selector scope="auto" active="linux-or-macos" ready=""><devsite-tabs role="tablist" connected="">

On Linux:

<pre class="lang-sh" translate="no" dir="ltr" is-upgraded=""><span class="pln">export GOOGLE_APPLICATION_CREDENTIALS</span><span class="pun">=</span><span class="str">"</span><var><span class="str">[PATH]</span></var><span class="str">"</span></pre>

For example:

<pre class="lang-sh" translate="no" dir="ltr" is-upgraded=""><span class="pln">export GOOGLE_APPLICATION_CREDENTIALS</span><span class="pun">=</span><span class="str">"/home/user/Downloads/</span><var><span class="str">my-key</span></var><span class="str">.json"</span></pre>


<section tab="windows" role="tabpanel" aria-labelledby="aria-tab-windows" tabindex="0" id="tabpanel-windows" class="sf-hidden">



</devsite-selector>

## Install and initialize the Cloud SDK

>**Note:** <span>You can skip this step if you will not be using the API.</span></aside>

If you plan to use the Dialogflow API, you need to install and initialize the Cloud SDK. Cloud SDK is a set of tools that you can use to manage resources and applications hosted on Google Cloud. This includes the [`gcloud`](https://cloud.google.com/sdk/gcloud) command line tool.

The following link provides instructions:

[Install and initialize the Cloud SDK](https://cloud.google.com/sdk/docs).

## Test the SDK and authentication

>**Note:** <span>You can skip this step if you will not be using the API.</span></aside>

If you have set up authentication in previous steps, you can use the `gcloud` tool to test your authentication environment. Execute the following command and verify that no error occurs and that credentials are returned:

<devsite-code no-copy="">

<pre translate="no" dir="ltr" is-upgraded="">gcloud auth application-default print-access-token</pre>



That command is used by all Dialogflow command line REST samples to authenticate API calls.

## Install the Dialogflow client library

```
pip install dialogflow
```