class VisitedPagesMiddleware:
    """
    Track users' visited pages
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request
        response = self.get_response(request)

        # Process the response only for authenticated users
        if request.user.is_authenticated:
            if "visited_pages" not in request.session:
                request.session["visited_pages"] = []

            if len(request.session["visited_pages"]) > 10:
                reversed = request.session["visited_pages"][::-1]
                reversed.pop()
                request.session["visited_pages"] = reversed[::-1]

            # Add the current page to the stack
            skip_paths = ["/", "/home/", "/accounts/login/", "/accounts/signup/", "/admin/", "/admin/jsi18n/", "/admin/login/"]
            skip_paths = [p.replace("/", "") for p in skip_paths]
            current_path = request.path
            current_path_re = str(request.path).replace("/", "")
            request_session_re = [
                p.replace("/", "") for p in request.session["visited_pages"]
            ]

            if (
                current_path_re not in skip_paths
                and current_path_re not in request_session_re
            ):
                request.session["visited_pages"].append(current_path)
            elif current_path in request.session["visited_pages"]:
                index = request.session["visited_pages"].index(current_path)
                page = request.session["visited_pages"].pop(index)
                request.session["visited_pages"].append(page)

            request.session.save()

        return response
