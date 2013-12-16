Changelog
---------

There's a frood who really knows where his towel is.

1.0rc2 (unreleased)
^^^^^^^^^^^^^^^^^^^

- Fix setattr when importing blog entries. [jpg]


1.0rc1 (2013-12-04)
^^^^^^^^^^^^^^^^^^^

- Set effective date when importing external blog entries [jpg] (closes #8181)

- Fix encoding when importing images [jpg]

- Avoid error if URL is not reachable when looking for images in a feed entry body [ericof]

- To avoid blocking (by Cloudflare) we set fake headers on our requests
  [ericof] 

- Added section method in ExternalBlogEntry (closes #7745) 
  [marcosfromero]

- Avoid error if text is empty [cleberjsantos]

1.0a7 (2013-08-02)
^^^^^^^^^^^^^^^^^^^

- Just create entries **if** they have an id [ericof]

1.0a6 (2013-07-24)
^^^^^^^^^^^^^^^^^^^

- Add a default view for ExternalBlog [ericof]

1.0a5 (2013-07-10)
^^^^^^^^^^^^^^^^^^^

- Fix a bug with image handling [ericof]


1.0a4 (2013-07-10)
^^^^^^^^^^^^^^^^^^^

- Fix a bug when no content body was provided in the feed [ericof]

- Style fix for partner code [ericof]

- Fix config checking [ericof]


1.0a3 (2013-06-03)
^^^^^^^^^^^^^^^^^^^

- Add image field to blog entry [ericof]

- Get image from original blog entry [ericof]


1.0a2 (2013-06-03)
^^^^^^^^^^^^^^^^^^

- Add fields to External Blog content type [ericof]

- Add a browser view to display blog status [ericof]

- Add a browser view to update all blogs [ericof]


1.0a1 (2013-05-02)
^^^^^^^^^^^^^^^^^^

- Initial release.
