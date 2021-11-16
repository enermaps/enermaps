require 'cgi'

module Precious
  module Views
    class Layout < Mustache
      include Rack::Utils
      include Sprockets::Helpers
      include Precious::Views::AppHelpers
      include Precious::Views::SprocketsHelpers
      include Precious::Views::RouteHelpers
      include Precious::Views::OcticonHelpers

      alias_method :h, :escape_html

      attr_reader :name, :path

      def escaped_name
        CGI.escape(@name)
      end

      def title
        "Home"
      end

      def has_path
        !@path.nil?
      end

      def base_url
        @base_url
      end

      def custom_path
        @base_url
      end

      def custom_css
        clean_url(custom_path, "custom.css")
      end

      def custom_js
        clean_url(custom_path, "custom.js")
      end

      def mathjax_config_path
        page_route(@mathjax_config)
      end

      def mathjax_js
        "#{page_route('gollum/assets/mathjax/MathJax.js')}?config=TeX-AMS-MML_HTMLorMML"
      end

      def css # custom css
        @css
      end

      def js # custom js
        @js
      end

      def critic_markup
        @critic_markup
      end

      def per_page_uploads
        @per_page_uploads
      end

      # Navigation bar
      def search
        false
      end

      def history
        false
      end

      def overview
        false
      end

      def latest_changes
        false
      end

      # Additional omniauth parameters for the user status bar, used in user.mustache
      def user_authed
        @user_authed
      end

      def user_provider
        @user.provider
      end

      def user_name
        @user.name
      end

    end
  end
end