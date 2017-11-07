require 'sinatra'
require 'json'

class HelloWorldApp < Sinatra::Base
  post '/payload' do
    push = JSON.parse(request.body.read)
    puts "I got some JSON: #{push.inspect}"
  end
end
