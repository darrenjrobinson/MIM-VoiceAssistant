# POST method: $req
$requestBody = Get-Content $req -Raw | ConvertFrom-Json
# Query from Speech to Text
$query = $requestBody.query
# Staging or Prod LUIS Search
$staging = $requestBody.staging 
# Flag to send constructed query to MIM or Not
$queryMIM = $false


if ($query -and $staging){
    # LUIS 
    $LUISSubURI = "https://yourAzureKeyVault.vault.azure.net/secrets/LUISSubscription/0f7b3bec6c564db6b91e2f13f734ecf7"
    $LUISKey = "https://yourAzureKeyVault.vault.azure.net/secrets/LUISKeyID/041c326bc146475093e5ee2fdd98918f"
    # MIM API Mgmnt
    $MIMAPIKey = "https://yourAzureKeyVault.vault.azure.net/secrets/MIMAPIMgmtAPIKey/b76d0031079347fe84ec623e48230170"

    # MSI Variables via Function Application Settings Variables
    # Endpoint and Password
    $endpoint = $env:MSI_ENDPOINT
    $secret = $env:MSI_SECRET

    # Vault URI to get AuthN Token
    $vaultTokenURI = 'https://vault.azure.net&api-version=2017-09-01'
    # Create AuthN Header with our Function App Secret
    $header = @{'Secret' = $secret}

    # Get Key Vault AuthN Token
    $authenticationResult = Invoke-RestMethod -Method Get -Headers $header -Uri ($endpoint +'?resource=' +$vaultTokenURI)

    # Use Key Vault AuthN Token to create Request Header
    $requestHeader = @{ Authorization = "Bearer $($authenticationResult.access_token)" }

    # Call the Vault and Retrieve LUIS Sub
    $subscriptionResp = Invoke-RestMethod -Method GET -Uri "$($LUISSubURI)/?api-version=2015-06-01" -ContentType 'application/json' -Headers $requestHeader
    $subscription = $subscriptionResp.value
    # Call the Vault and Retrieve LUIS Key
    $appIDResp = Invoke-RestMethod -Method GET -Uri "$($LUISKey)/?api-version=2015-06-01" -ContentType 'application/json' -Headers $requestHeader
    $appID = $appIDResp.value
    # MIM API Mgment Access Secret
    $MIMSecretResp = Invoke-RestMethod -Method GET -Uri "$($MIMAPIKey)/?api-version=2015-06-01" -ContentType 'application/json' -Headers $requestHeader
    $MIMAPIsecret = $MIMSecretResp.value

    # LUIS URI to send Speech to for analysis
    $URI = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/$($appID)?subscription-key=$($subscription)&staging=$($staging)&verbose=true&timezoneOffset=600&q=$($query)" 
    # Response Flag
    [boolean]$queryResponse = $false 
    # Submit Query
    $response = Invoke-RestMethod -Method Get -Uri $URI -UseBasicParsing -Verbose
    $response.intents
    $response.entities
    if ($response -and $response.entities){
        foreach ($entity in $response.entities){
            switch ($entity.type){
                "UserStatus" {$entitlement = $entity.entity}
                "Entitlement" {$entitlement = $entity.entity}
                "Fullname::firstname" {$firstname = $entity.entity}
                "Fullname::lastname" {$lastname = $entity.entity}
            }
        }
        $queryResponse = $true 
    } 

   if ($queryResponse) {
        if ($firstname -and $lastname){
            $fullname = $firstname + " " + $lastname
            "Fullname: $($fullname)"
        }

        if ($entitlement -and $fullname){
            "The query is for $($fullname) about $($entitlement)"
            $queryMIM = $true
        } else {
            $output = "Entitlement: $($entitlment) Fullname: $($fullname)"
        }
   } else {
       $output = "No Entitlement/Entity returned: $($queryResponse)"
   }
 
    # Query MIM via Azure API Management
    if ($queryMIM){

        $MIMquery = "Person[DisplayName='$($fullname)']"
        $MIMquery        
        $MIMqueryEncoded = [System.Web.HttpUtility]::UrlEncode($MIMquery)

        $MIMAPIURL = "https://YourAPIName.azure-api.net/YourAPIMgmtAppName/v2/resources/?filter=/$($MIMqueryEncoded)" 
        $Headers = @{'Ocp-Apim-Subscription-Key' = $MIMAPIsecret} 
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

        $userResponse = Invoke-RestMethod -Uri $MIMAPIURL -Headers $Headers -ContentType "application/json" -UseBasicParsing -Method Get
        $userResponse
    }

}


# ------------------------------------------------------
#
#  LOGIC for response
#
# ------------------------------------------------------

if ($userResponse -and ($entitlement.Equals('mailbox'))){
    if ($userResponse.results.Email){
        $speechText = "yes they have a mailbox. Their email address is $($userResponse.results.Email)"
    } else {
        $speechText = "no, they don't have a mailbox"
    }
} elseif ($userResponse -and ($entitlement.Equals('active directory account'))) {
    if ($userResponse.results.AccountName){
        $speechText = "yes they have an Active Directory Account. Their login ID is $($userResponse.results.AccountName)"
    } else {
        $speechText = "no, they do not have an Active Directory Account"
    }    
}  elseif ($userResponse -and ($entitlement.Equals('expiry date'))) {
    if ($userResponse.results.EmployeeEndDate){
        
        [datetime]$endDate = $userResponse.results.EmployeeEndDate
        $endDay = $endDate.Day
        $endMonth = $endDate.Month
        $endYear = $endDate.Year

        switch ($endMonth){
            "1" {$endMonthout = "January"}
            "2" {$endMonthout = "February"}
            "3" {$endMonthout = "March"}
            "4" {$endMonthout = "April"}
            "5" {$endMonthout = "May"}
            "6" {$endMonthout = "June"}
            "7" {$endMonthout = "July"}
            "8" {$endMonthout = "August"}
            "9" {$endMonthout = "September"}
            "10" {$endMonthout = "October"}
            "11" {$endMonthout = "November"}
            "12" {$endMonthout = "December"}
        }

        $speechText = "yes they have an End Date. Their End Date is $($endDay) $($endMonthout) $($endYear)"

    } else {
        $speechText = "no, they do not have an End Date"
    }    
}
else {
    $speechText = "I was unable to interpret your query. Please try again"
    $userResponse.results
    $entitlement
}

$speechText
Out-File -Encoding Ascii -FilePath $res -inputObject $speechText
