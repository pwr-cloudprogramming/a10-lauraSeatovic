provider "aws" {
  region = "us-east-1"
}

resource "aws_cognito_user_pool" "tic_tac_toe_user_pool" {
  name = "tic_tac_toe-user-pool"
  auto_verified_attributes = ["email"]
  username_attributes = [ "email" ]
  schema {
    attribute_data_type = "String"
    mutable             = true
    name                = "name"
    required            = true
  }
  schema {
    attribute_data_type = "String"
    mutable             = true
    name                = "email"
    required            = true
  }

  password_policy {
    minimum_length    = "8"
  }
  mfa_configuration        = "OFF"
}

resource "aws_cognito_user_pool_client" "tic_tac_toe_user_pool_client" {
  name = "tic_tac_toe-client"
  user_pool_id = aws_cognito_user_pool.tic_tac_toe_user_pool.id
  generate_secret = false
  explicit_auth_flows = ["USER_PASSWORD_AUTH"]
}

resource "aws_cognito_user_pool_domain" "tic_tac_toe_user_pool_domain" {
  domain = "tic-tac-toe-domain"
  user_pool_id = aws_cognito_user_pool.tic_tac_toe_user_pool.id
}
