Gollum::Page.send :remove_const, :FORMAT_NAMES if defined? Gollum::Page::FORMAT_NAMES

## Omni Auth
require 'omnigollum'
require 'omniauth/strategies/github'

# https://github.com/gollum/gollum/wiki/Sample-config.rb
wiki_options = {
  :allow_uploads => true,
  :allow_editing => true,
  :css => true,
  :js => true,
  :h1_title => true,
}
Precious::App.set(:wiki_options, wiki_options)

options = {
  # OmniAuth::Builder block is passed as a proc
  :providers => Proc.new do
    provider :github, ENV['GITHUB_CLIENT_ID'], ENV['GITHUB_CLIENT_SECRET'], {:scope => 'read:user,user:email'}
  end,
  :dummy_auth => false,

  # Specify committer name as just the user name
  :author_format => Proc.new { |user| user.name },
  # Specify committer e-mail as just the user e-mail
  :author_email => Proc.new { |user| user.email },

  # Authorized users
  :authorized_users => ENV["AUTH_USERS"].split(","),
}

## For GitHub Auth to work properly
OmniAuth.config.allowed_request_methods = [:post, :get]

## :omnigollum options *must* be set before the Omnigollum extension is registered
Precious::App.set(:omnigollum, options)
Precious::App.register Omnigollum::Sinatra

# Hook to be invoked after a commit
Gollum::Hook.register(:post_commit, :hook_id) do |committer, sha1|
  `sh /root/app/scripts/fetch-pull`
  `sh /root/app/scripts/push`
end
