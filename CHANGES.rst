Changelog of lizard-fewsunblobbed
=================================


2.4 (unreleased)
----------------

- Nothing changed yet.


2.3 (2012-10-18)
----------------

- Add location search button.


2.2 (2012-10-04)
----------------

- Add flot graph support.

- Add location search support.

- Add icon to legend.


2.1 (2012-05-29)
----------------

- Popup styling.


2.0 (2012-05-18)
----------------

- Some technical fixes.

- Add .gitignore and MANIFEST.in

- Fix path in manifest.in.

- Remove various dumpfiles

- Move fews_unblobbed_cache management command to tasks.py

- Add dependency on lizard-task to setup.py

- Added edit link

- Updated layout for bootstrap.

- Changed .txt extensions to .rst.


1.25 (2011-11-21)
-----------------

- Rather gross hacks that turn the IconStyle model into a class that
  acts as if it's a model with an empty database behind it. The reason
  for this is that the current IconStyle implementation doesn't work
  (it wants to put data into the fews-unblobbed database, which is
  readonly and not under our control), but should be fixed soonish.


1.24 (2011-11-04)
-----------------

- Removed hack for http://code.djangoproject.com/ticket/12999 in AlarmRouter, as it is fixed in
  Django versions >= 1.2.

- Added hack for https://code.djangoproject.com/ticket/16353 in AlarmRouter, it was breaking tests.

- Increased version dependency for lizard_map (to 3.3) and lizard_ui (to 3.6)

- Modified views.py, templates to class based views for lizard_map 3.3 compatibility

- Added version dependency to lizard_map and lizard_ui.

- Added option for admin IconStyles.

- Added IconStyle model and migration. Icons are now configurable. It
  will revert to a default when nothing is configurated.

Note: When upgrading, run: bin/django syncdb --database=fews-unblobbed


1.23 (2011-06-30)
-----------------

- Changed graph: now uses standard Graph.legend. The legend is
  displayed on top of the graph. #2990

- Moved filter.parameters calculation to model Filter.

- Added filter.parameters to fews_unblobbed_cache management command.


1.22 (2011-06-22)
-----------------

- Fixed #2949: Changed coordinates to lon/lat prevents disappearing
  icons.


1.21 (2011-06-21)
-----------------

- Fixed #2942: If the number of items is too large, the graph will not
  plot balls anymore.


1.20 (2011-06-21)
-----------------

- Added management command fews_unblobbed_copy_data to copy data for
  demo purposes.

- Fixed #2927: Clicking on filters result in parameters from all
  subfilters.

- Added styling for demo filter map icons.


1.19 (2011-06-17)
-----------------

- Workspace items for filters that aren't found don't "404" the entire site
  anymore.

- Raising a WorkspaceItemError in the adapter when the filter/parameter
  combination doesn't exist anymore. This removes the workspaceitem from the
  workspace automatically, preventing stuck sites.


1.18 (2011-06-17)
-----------------

- Implemented extend() in the adapter.

- Adding unit as the default y-axis label.


1.17 (2011-06-16)
-----------------

- Filter parents are now clickable. The result is all parameters of
  the filter and its descendants.
- Explicitly order Timeseriedata by date, otherwise graphs with FEWS time
  series can display a tangled mess of lines (ticket 2908)


1.16 (2011-06-03)
-----------------

- Depending on lizard-ui > 1.64 as that allows us to not pass along the full
  filter tree when viewing one specific filter item: it saves on the transfer
  time.

- Depending on lizard-map >= 1.80 now as that does away with the javascript
  map hover handler. More performance!

- Removed Timeseriedata from admin. See #2590.


1.15 (2011-05-03)
-----------------

- Disabled the legend borders of popup form.


1.14 (2011-04-28)
-----------------

- Quick fix of legend for demo.


1.13 (2011-04-28)
-----------------

- Quick fix of legend for demo.


1.12 (2011-04-27)
-----------------

- Changed graph lines to 'o-' (dot-line).

- Removed unused imports.


1.11 (2011-04-21)
-----------------

- Removed unnecessary workspace_manager and date_range_form stuff. It
  is also incompatible with map >= 1.71.


1.10 (2011-03-09)
-----------------

- Added fews_unblobbed_cache management command. This enables cronjob
  to regularly refresh the cache. Two levels of cache are implemented:
  filter tree and Timeserie.has_data_dict. This greatly enhances the
  user experience.


1.9 (2011-02-14)
----------------

- Fixed breadcrumbs bug.


1.8 (2011-02-01)
----------------

- Added option crumbs_prepend (see lizard_ui).


1.7 (2011-01-31)
----------------

- Fixed bug for endnodes at the root of the filtertree.


1.6 (2010-12-15)
----------------

- Added hack that works around mapnik bug: we draw every point four times.
  One in the right location, three with 10cm offsets.


1.5 (2010-12-14)
----------------

- Added tests.


1.4 (2010-12-14)
----------------

- Added option to exclude filters from your filters
  tree. FEWS_UNBLOBBED_EXCLUDE_FILTERS in your settings.py.


1.3 (2010-12-09)
----------------

- Enabled default click handler on base fews browser page.

- Solved #2148 by 'merging' Meta classes in model definitions.


1.2 (2010-09-22)
----------------

- Add extra check when timeserie(filter, location, parameter) returns
  multiple results. This should never occur, but occurs when using a clients database.


1.1 (2010-09-03)
----------------

- Django-treebeard: we need 1.61 minimum.

- Fixed up the models: no more TextFields where we really need charfields.

- Added a get_database_engine() that picks up the correct database engine for
  treebeard.


1.0 (2010-08-30)
----------------

- Enabled hovering over points so that you get names.

- Improved test setup.


0.10 (2010-08-18)
-----------------

- Updated adapter to current lizard-map.

- Added several graph options to adapter.

- Adjusted test setup to use nose and unittests.


0.9 (2010-07-16)
----------------

- Greatly improve performance of adapter.layer.


0.8 (2010-07-15)
----------------

- Search points is now generic and uses function in lizard-map.
- Adapter.image function now accepts layout options: y_min, y_max,
  line_min, line_max, line_avg, colors, title.
- Implement adapter.symbol function.


0.7 (2010-06-24)
----------------

- Fixed bug: we're including the workspace id in addition to the workspaceitem
  id. This fixes a bug when first viewing a graph in a temp workspace.


0.6 (2010-06-23)
----------------

- Using django's cache framework to cache the expensive filter tree (currently
  for 8 hours).

- Huge speed increase for the parameter list as we're using django's ``__``
  tricks in the query now instead of looping by hand.

- Added Timeserie display/search caching.


0.5 (2010-06-23)
----------------

- Using lizard-ui's ajax loading and lizard-map's generic workspace drag/drop
  now.  This means we can render a full fews-browser page ourselves including
  all interaction.

- Added graph and search functions.

- Switched layer display and search functions to lizard-map's new adapter
  approach.

- Added visual feedback whether points actually have data.

- Using lizard-ui's generic sidebar accordion for the fews browser page.


0.4 (2010-05-18)
----------------

- Added basic point search function.

- Added mapnik layer rendering function.

- Added dependency on lizard-map.


0.3 (2010-04-14)
----------------

- Tree fixes.


0.2 (2010-04-13)
----------------

- Added utility methods for legend names and so.

- Adjusted __unicode__ string representations.

- Fixed generated field types (not everything is a text area).


0.1 (2010-04-06)
----------------

- First working version: added models.py
- Initial library skeleton created by nensskel.  [jack]
